from logging import getLogger

from ..worker import run
from ...commands.args import WEB, UPLOAD
from ...commands.upload import STREAM, NAME, upload_files
from ...lib.log import Record

log = getLogger(__name__)


class Upload:

    def __init__(self, config):
        self.__config = config

    def __call__(self, request, s):
        files = [{NAME: file.filename, STREAM: file.stream} for file in request.files.getlist('files')]
        items = request.form.getlist('kit')
        # we do this in two stages
        # first, immediate saving of files while web browser waiting for response
        upload_files(Record(log), self.__config, files=files, items=items)
        # second, start rest of ingest process in background
        run(self.__config, UPLOAD, Upload, f'{WEB}-{UPLOAD}.log')
