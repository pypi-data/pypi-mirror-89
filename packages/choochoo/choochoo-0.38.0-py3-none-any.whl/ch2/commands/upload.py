from glob import glob
from logging import getLogger
from os import makedirs
from os.path import basename, join, exists, dirname

from ..commands.args import KIT, PATH, DATA, UPLOAD, PROCESS, CPROFILE
from ..common.date import time_to_local_time, Y, YMDTHMS
from ..common.io import touch, clean_path, data_hash
from ..common.log import log_current_exception
from ..lib.io import split_fit_path
from ..lib.log import Record
from ..lib.utils import timing
from ..pipeline.process import run_pipeline
from ..pipeline.read.utils import AbortImportButMarkScanned
from ..sql import KitItem, FileHash, PipelineType

log = getLogger(__name__)


TYPE = 'type'
TIME = 'time'
STREAM = 'stream'
DATA = 'data'
EXTRA = 'extra'
HASH = 'hash'
NAME = 'name'
ACTIVITY = 'activity'
MONITOR = 'monitor'
SPORT = 'sport'
DIR = 'dir'
DOT_FIT = '.fit'
READ_PATH = 'read-path'
WRITE_PATH = 'write-path'


def upload(config):
    '''
## upload

    > ch2 upload --kit ITEM [ITEM...] -- PATH [PATH ...]

Copy FIT files, storing the data in the permanent store on the file system.
Optionally, call process after, to add data to the database.
Both monitor and activity files are accepted.

### Examples

    > ch2 upload --kit cotic -- ~/fit/2018-01-01.fit

will store the given file, add activity data to the database (associated with the kit 'cotic'), check for
new monitor data, and update statistics.
    '''
    args = config.args
    with timing(UPLOAD):
        upload_files(Record(log), config, files=open_files(args[PATH]), items=args[KIT])
        if args[PROCESS]:
            run_pipeline(config, PipelineType.PROCESS, cprofile=args[CPROFILE])


class SkipFile(Exception):
    pass


def open_files(paths):
    # use an iterator here to avoid opening too many files at once
    for path in paths:
        path = clean_path(path)
        if exists(path):
            name = basename(path)
            log.debug(f'Reading {path}')
            stream = open(path, 'rb')
            yield {STREAM: stream, NAME: name, READ_PATH: path}
        else:
            raise Exception(f'No file at {path}')


def check_items(s, items):
    for item in items:
        if not s.query(KitItem).filter(KitItem.name == item).one_or_none():
            raise Exception(f'Kit item {item} does not exist')


def read_file(file):
    # add DATA to dicts with STREAM
    log.debug(f'Reading {file[NAME]}')
    file[DATA] = file[STREAM].read()
    file[STREAM].close()


def hash_file(file):
    # add HASH to dicts with DATA
    log.debug(f'Hashing {file[NAME]}')
    file[HASH] = data_hash(file[DATA])
    log.debug(f'Hash of {file[NAME]} is {file[HASH]}')


def check_path(file):
    path, name = file[WRITE_PATH], file[NAME]
    gpath, _ = split_fit_path(path)
    match = glob(gpath)
    if match:
        touch(match[0])  # trigger re-processing
        raise SkipFile(f'A file already exists for {name} at {match[0]}')
    log.debug(f'File {name} cleared for path {path}')


def check_hash(s, file):
    hash, path, name = file[HASH], file[WRITE_PATH], file[NAME]
    file_hash = s.query(FileHash).filter(FileHash.hash == hash).one_or_none()
    if file_hash and file_hash.file_scan:
        raise SkipFile(f'A file was already processed with the same hash as {name} '
                       f'({hash} at {file_hash.file_scan.path})')
    log.debug(f'File {name} cleared for hash {hash}')


def check_file(s, file):
    check_path(file)
    check_hash(s, file)


def parse_fit_data(file, items=None):
    from ch2.pipeline.read.monitor import MonitorReader
    from ch2.pipeline.read.activity import ActivityReader
    try:
        # add TIME and TYPE and EXTRA (and maybe SPORT) given (fit) DATA and NAME
        try:
            records = MonitorReader.parse_records(file[DATA])
            file[TIME] = MonitorReader.read_first_timestamp(file[NAME], records)
            file[TYPE] = MONITOR
            # don't use '-' here or it will be treated as kit in path matching
            file[EXTRA] = ':' + file[HASH][0:5]
            log.debug(f'File {file[NAME]} contains monitor data')
        except AbortImportButMarkScanned:
            records = ActivityReader.parse_records(file[DATA])
            file[TIME] = ActivityReader.read_first_timestamp(file[NAME], records)
            file[SPORT] = ActivityReader.read_sport(file[NAME], records)
            file[TYPE] = ACTIVITY
            file[EXTRA] = '-' + ','.join(items) if items else ''
            log.debug(f'File {file[NAME]} contains activity data')
    except Exception as e:
        log_current_exception()
        raise Exception(f'Could not parse {file[NAME]} as a fit file')


def build_path(data_dir, file):
    # add PATH given TIME, TYPE, SPORT and EXTRA
    date = time_to_local_time(file[TIME], fmt=YMDTHMS)
    year = time_to_local_time(file[TIME], fmt=Y)
    file[DIR] = join(data_dir, file[TYPE], year)
    if SPORT in file: file[DIR] = join(file[DIR], file[SPORT])
    file[WRITE_PATH] = join(file[DIR], date + file[EXTRA] + DOT_FIT)
    log.debug(f'Target directory is {file[DIR]}')


def write_file(file):
    try:
        dir = dirname(file[WRITE_PATH])
        if not exists(dir):
            log.debug(f'Creating {dir}')
            makedirs(dir)
        if exists(file[WRITE_PATH]):
            log.warning(f'Overwriting data at {file[WRITE_PATH]}')
        with open(file[WRITE_PATH], 'wb') as out:
            log.info(f'Writing {file[NAME]} to {file[WRITE_PATH]}')
            out.write(file[DATA])
    except Exception as e:
        log_current_exception()
        raise Exception(f'Could not save {file[NAME]}')


def upload_files(record, data, files=tuple(), items=tuple()):
    with record.record_exceptions():
        with data.db.session_context() as s:
            data_dir = data.args._format_path(DATA)
            check_items(s, items)
            for file in files:
                try:
                    read_file(file)
                    hash_file(file)
                    parse_fit_data(file, items=items)
                    build_path(data_dir, file)
                    check_file(s, file)
                    write_file(file)
                    record.info(f'Uploaded {file[NAME]} to {file[WRITE_PATH]}')
                except SkipFile as e:
                    record.warning(e)
