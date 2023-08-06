
from ..database import add_process
from ..profile import Profile
from ...pipeline.read.activity import ActivityReader
from ...pipeline.read.garmin import GarminReader
from ...pipeline.read.monitor import MonitorReader
from ...sql.types import short_cls


def garmin(config):
    '''
## garmin

This extends the default configuration with download of monitor data from Garmin.

It requires the user and password to be defined as constants.
    '''
    Garmin(config).load()


class Garmin(Profile):

    def _load_read_pipeline(self, s):
        sport_to_activity = self._sport_to_activity()
        record_to_db = self._record_to_db()
        add_process(s, ActivityReader, owner_out=short_cls(ActivityReader),
                    sport_to_activity=sport_to_activity, record_to_db=record_to_db)
        monitor_reader = add_process(s, MonitorReader)
        # add these, chained so that we load available data (know what is missing),
        # download new data, and load new data
        garmin_reader = add_process(s, GarminReader, blocked_by=[monitor_reader])
        add_process(s, MonitorReader, blocked_by=[garmin_reader])
