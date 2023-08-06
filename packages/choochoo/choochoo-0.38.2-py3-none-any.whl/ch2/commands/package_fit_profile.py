
from logging import getLogger

from .args import PATH, WARN
from ..fit.profile.profile import pickle_profile
from ..common.io import clean_path

log = getLogger(__name__)


def package_fit_profile(config):
    '''
## package-fit-profile

    > ch2 package-fit-profile data/sdk/Profile.xlsx

Parse the global profile and save the structures containing types and messages
to a pickle file that is distributed with this package.

This command is intended for internal use only.
    '''
    args = config.args
    in_path, warn = clean_path(args[PATH]), args[WARN]
    pickle_profile(in_path, warn=warn)
