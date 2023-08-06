
from logging import getLogger

from ..common.date import to_time
from ..sql import ActivityBookmark, ActivityGroup, StatisticName
from ..sql.database import connect

log = getLogger(__name__)


class CoastingBookmark:

    def __init__(self, db):
        self._db = db

    def run(self, kit, min_time, max_cadence, min_speed, group, constraint=None):
        with self._db.session_context() as s:
            self.__delete_previous(s, constraint)
            for aj_id, start, finish in self.__find(s, kit, min_time, max_cadence, min_speed, group):
                self.__add(s, aj_id, start, finish, constraint)

    def __delete_previous(self, s, constraint):
        s.query(ActivityBookmark). \
            filter(ActivityBookmark.owner == self,
                   ActivityBookmark.constraint == constraint). \
            delete()

    def __add(self, s, aj_id, start, finish, constraint):
        log.info('%s - %s (%d)' % (to_time(start), to_time(finish), aj_id))
        s.add(ActivityBookmark(activity_journal_id=aj_id, start=start, finish=finish,
                               owner=self, constraint=constraint))

    def __find(self, s, kit, min_time, max_cadence, min_speed, group):

        from ..pipeline.owners import ActivityReader

        group = ActivityGroup.from_name(s, group)
        cadence_statistic = StatisticName.from_name(s, 'Cadence', ActivityReader, group)
        distance_statistic = StatisticName.from_name(s, 'Distance', ActivityReader, group)
        speed_statistic = StatisticName.from_name(s, 'Speed', ActivityReader, group)
        kit_statistic = StatisticName.from_name(s, ActivityReader.Kit, ActivityReader, group)
        s.execute('PRAGMA automatic_index=OFF;')
        for row in s.execute('''
select t.activity_journal_id, s.time, f.time
  from statistic_journal as ks,
       statistic_journal_text as kt,
       activity_timespan as t cross join  -- this tweaked the plan
       statistic_journal as s,
       statistic_journal_integer as si,
       statistic_journal as ss,
       statistic_journal_integer as ssi,
       statistic_journal as f,
       statistic_journal_integer as fi,
       statistic_journal as ff,
       statistic_journal_integer as ffi
 where ks.source_id = t.activity_journal_id
   and ks.statistic_name_id = :kit_statistic
   and ks.id = kt.id
   and kt.value = :kit
   -- s and ss bracket the change in cadence at the start
   -- f and ff bracket the change in cadence at the finish
   and s.statistic_name_id = :cadence_statistic
   and f.statistic_name_id = :cadence_statistic
   and ss.statistic_name_id = :cadence_statistic
   and ff.statistic_name_id = :cadence_statistic
   and s.id = si.id
   and f.id = fi.id
   and ss.id = ssi.id
   and ff.id = ffi.id
   and si.value < :max_cadence
   and fi.value < :max_cadence
   and ss.serial = s.serial-1
   and ff.serial = f.serial+1
   and s.source_id = t.activity_journal_id
   and ss.source_id = t.activity_journal_id
   and f.source_id = t.activity_journal_id
   and ff.source_id = t.activity_journal_id
   and ssi.value >= :max_cadence
   and ffi.value >= :max_cadence
   and f.time - s.time > :min_time
   and t.start < s.time
   and t.finish > f.time
   -- limit cadence between s and f
   and not exists (select 1
                     from statistic_journal_integer as ji,
                          statistic_journal as j
                    where ji.value >= :max_cadence
                      and ji.id = j.id
                      and j.statistic_name_id = :cadence_statistic
                      and j.source_id = s.source_id
                      and j.serial > s.serial
                      and j.serial < f.serial)
   -- limit average speed
   and exists (select 1
                 from statistic_journal_float as f1,
                      statistic_journal_float as f2,
                      statistic_journal as j1,
                      statistic_journal as j2
                where f1.id = j1.id
                  and f2.id = j2.id
                  and j1.statistic_name_id = :distance_statistic
                  and j2.statistic_name_id = :distance_statistic
                  and j1.serial = s.serial
                  and j2.serial = f.serial
                  and j1.source_id = f.source_id
                  and j2.source_id = f.source_id
                  and f2.value - f1.value > :min_speed * (f.time - s.time))
   -- exclude stationary points 
   and not exists (select 1
                     from statistic_journal_float as jf,
                          statistic_journal as j
                    where jf.value = 0
                      and jf.id = j.id
                      and j.statistic_name_id = :speed_statistic
                      and j.source_id = s.source_id
                      and j.serial >= s.serial
                      and j.serial <= f.serial)
 order by t.activity_journal_id;  -- doesn't affect speed and makes duplicates easier to see
        ''', {'min_time': min_time, 'max_cadence': max_cadence, 'min_speed': min_speed, 'kit': kit,
              'group': str(group), 'cadence_statistic': cadence_statistic.id, 'speed_statistic': speed_statistic.id,
              'distance_statistic': distance_statistic.id, 'kit_statistic': kit_statistic.id}):
            yield row[0], row[1], row[2]
        s.execute('PRAGMA automatic_index=ON;')


if __name__ == '__main__':
    '''
    Bookmark sections of activities that exceed 60s of little or no pedalling (maximum cadence 20)
    and with any speed (max 0).
    
    These are then used in the fit_power_parameters template to estimate CdA and Crr. 
    '''
    db = connect(['-v 4'])
#    CoastingBookmark(db).run('cotic', 60, 20, 0, 'bike', constraint='cotic 60/20/0')
    CoastingBookmark(db).run('cotic', 15, 5, 10, 'bike', constraint='cotic 15/5/10')
