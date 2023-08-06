
from logging import getLogger
from os.path import join, dirname
from pickle import load, dump

import openpyxl as xls
from pkg_resources import resource_stream

from .messages import Messages
from .support import NullableLog
from .types import Types
from ...commands.args import PACKAGE_FIT_PROFILE

log = getLogger(__name__)
PROFILE_NAME = 'global-profile.pkl'
PROFILE = []


def read_external_profile(path, warn=False):
    nlog = NullableLog(log)
    wb = xls.load_workbook(path)
    types = Types(nlog, wb['Types'], warn=warn)
    messages = Messages(nlog, wb['Messages'], types, warn=warn)
    return nlog, types, messages


def read_internal_profile():
    if not PROFILE:
        log.debug('Unpickling profile')
        try:
            input = resource_stream(__name__, PROFILE_NAME)
            PROFILE.append(load(input))
            input.close()
        except FileNotFoundError:
            log.warning('There was a problem reading the pickled profile.')
            log.warning('If you installed via pip then please create an issue at')
            log.warning('https://github.com/andrewcooke/choochoo for support.')
            log.warning('If you installed via git please see `ch2 help %s`' % PACKAGE_FIT_PROFILE)
            raise Exception('Could not read %s (see log for more details)' % PROFILE_NAME)
        PROFILE[0][0].set_log(log)
    return PROFILE[0][1:]


def read_profile(warn=False, profile_path=None):
    if profile_path:
        log.debug('Reading profile from %s' % profile_path)
        _nlog, types, messages = read_external_profile(profile_path, warn=warn)
    else:
        types, messages = read_internal_profile()
    log.debug('Read profile')
    return types, messages


def read_fit(fit_path):
    log.debug('Reading fit file from %s' % fit_path)
    with open(fit_path, 'rb') as input:
        return input.read()


def pickle_profile(in_path, warn=False):
    log.info('Reading from %s' % in_path)
    nlog, types, messages = read_external_profile(in_path, warn=warn)
    out_path = join(dirname(__file__), PROFILE_NAME)
    nlog.set_log(None)
    log.info('Writing to %s' % out_path)
    with open(out_path, 'wb') as output:
        dump((nlog, types, messages), output)
    # test loading
    log.info('Test loading from %r' % PROFILE_NAME)
    log.info('Loaded %s, %s' % read_internal_profile())
