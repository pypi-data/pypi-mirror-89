
import datetime as dt
from tests import LogTestCase

from ch2.common.date import to_date
from ch2.lib.schedule import Schedule, DateOrdinals, POS_INFINITY


class TestRepeating(LogTestCase):

    def assert_str(self, x1, s):
        s1 = str(x1)
        self.assertEqual(s1, s)
        x2 = Schedule(s1)
        s2 = str(x2)
        self.assertEqual(s1, s2)

    def assert_bad(self, f, *args):
        with self.assertRaises(Exception):
            f(*args)

    def test_specification(self):
        # from the spec doc
        self.assert_str(Schedule('m[2Tue]'), 'm[2tue]')
        self.assert_str(Schedule('2m[2Tue]'), '2m[2tue]')
        self.assert_str(Schedule('1/2m[2Tue]'), '1/2m[2tue]')
        self.assert_str(Schedule('m[2Tue]1970-01-01-1970-12-31'), 'm[2tue]1970-01-01-1970-12-31')
        self.assert_str(Schedule('2018-07-05/5d[]'), '2/5d')
        self.assert_str(Schedule('d2018-07-05'), '2018-07-05')
        # others
        self.assert_str(Schedule('1/2w[1]2018-01-01-'), '1/2w[1]2018-01-01-')
        self.assert_str(Schedule('1/2w[2Mon,Fri,2,3]-1970-01-01'), '1/2w[2,3,fri,2mon]-1970-01-01')
        # some errors
        self.assert_bad(Schedule, '1/2[]2018-01-01-')   # must specify type
        self.assert_bad(Schedule, '1/2w[1d]2018-01-01-')  # no longer support type in location
        # some additional shortcuts for easier config
        self.assert_str(Schedule('-2019-10-07'), '-2019-10-07')
        self.assert_str(Schedule('2019-10-07-'), '2019-10-07-')
        self.assert_str(Schedule('2019-10-07'), '2019-10-07')

    def assert_at(self, spec, date, at_location):
        date = to_date(date)
        self.assertEqual(Schedule(spec).at_location(date), at_location)

    def test_day(self):
        self.assert_at('d', '2018-07-06', True)
        self.assert_at('d', '2018-07-07', True)
        self.assert_at('2d', '2018-07-06', True)
        self.assert_at('2d', '2018-07-07', True)
        self.assert_at('2d[1]', '2018-07-06', True)
        self.assert_at('2d[2]', '2018-07-06', False)
        self.assert_at('2d[3]', '2018-07-06', False)
        self.assert_at('2d[1]', '2018-07-07', False)
        self.assert_at('2d[2]', '2018-07-07', True)
        self.assert_at('2d[Fri]', '2018-07-06', True)
        self.assert_at('2d[Mon]', '2018-07-06', False)
        self.assert_at('2d[Fri]2018-07-06', '2018-07-06', True)
        self.assert_at('2d[Fri]2018-07-07', '2018-07-06',  False)
        self.assert_at('2d[Fri]2018-07-06-2018-07-07', '2018-07-06', True)
        self.assert_at('2d[Fri]2018-07-07-2018-07-08', '2018-07-06', False)
        self.assert_at('2d[Fri]2018-07-05-2018-07-06', '2018-07-06', False)
        self.assert_at('2018-10-10/3d[1,fri]', '2018-10-10', True)
        self.assert_at('2018-10-10/3d[1,fri]', '2018-10-11', False)
        self.assert_at('2018-10-10/3d[1,fri]', '2018-10-12', True)

    def test_week(self):
        self.assert_at('2018-07-06/w[Fri]', '2018-07-06', True)
        self.assert_at('2018-07-06/w[Fri]', '2018-07-05', False)
        self.assert_at('2018-07-06/w[Fri]', '2018-07-07', False)
        self.assert_at('2018-07-06/w[1]', '2018-07-02', True)
        self.assert_at('2018-07-06/w[1]', '2018-07-01', False)
        self.assert_at('2018-07-06/w[1]', '2018-07-03', False)
        self.assert_at('2018-07-06/w', '2018-07-02', True)
        self.assert_at('2018-07-06/w', '2018-07-01', True)
        self.assert_at('2018-07-06/w', '2018-07-03', True)
        # bug in diary
        self.assert_at('0/1w[1sun]', '2018-07-29', True)

    def test_month(self):
        self.assert_at('m[Sat]', '2018-07-07', True)
        self.assert_at('m[2]', '2018-07-02', True)
        self.assert_at('m[2]', '2018-07-01', False)
        self.assert_at('m', '2018-07-02', True)
        # numbering is different for months.  "2nd sunday" may not be in 2nd week.
        self.assert_at('m[1sat]', '2018-09-01', True)
        self.assert_at('m[1sun]', '2018-09-02', True)
        self.assert_at('m[1mon]', '2018-09-03', True)
        self.assert_at('m[1fri]', '2018-09-07', True)
        self.assert_at('m[2sat]', '2018-09-08', True)
        # bug seen in output from test_schedule command
        self.assert_at('m[mon,tue,5]', '2018-10-08', True)

    def test_year(self):
        self.assert_at('2018-07-07/y', '2018-07-02', True)

    def test_start_finish(self):
        p = Schedule('2018-07-08/2d2018-07-08-2018-07-09')
        self.assertEqual(p.start, dt.date(2018, 7, 8))
        p.start = None
        self.assertTrue(p.start is None)
        self.assertEqual(p.finish, dt.date(2018, 7, 9))

    def test_ordinals(self):
        d = dt.date(2018, 7, 25)
        o = DateOrdinals(d)
        self.assertEqual(o.dow, 2)  # wed

    def test_frame_start(self):
        s = Schedule('2018-01-01/2y')
        self.assertEqual(s.start_of_frame('2018-01-02'), to_date('2018-01-01'))
        self.assertEqual(s.start_of_frame('2017-01-02'), to_date('2016-01-01'))

    def test_extended(self):
        # from the spec doc
        self.assert_str(Schedule('x2018-10-07-'), 'x2018-10-07-')
        self.assert_str(Schedule('x[1,2,3]2020-03-06-'), 'x[1,2,3]2020-03-06-')
        self.assert_str(Schedule('x[fri]2020-03-06-'), 'x[fri]2020-03-06-')
        self.assert_bad(Schedule, 'x[1,2,3]')  # no range start
        self.assert_bad(Schedule, '2018-10-07x')  # no offset
        self.assert_bad(Schedule, '2x')  # no multiple repeat
        self.assert_at('x', '2018-07-06', True)
        # single day range
        self.assert_at('x2018-07-06', '2018-07-05', False)
        self.assert_at('x2018-07-06', '2018-07-06', True)
        self.assert_at('x2018-07-06', '2018-07-07', False)
        # from date onwards
        self.assert_at('x2018-07-06-', '2018-07-05', False)
        self.assert_at('x2018-07-06-', '2018-07-06', True)
        self.assert_at('x2018-07-06-', '2018-07-07', True)
        # until date
        self.assert_at('x-2018-07-06', '2018-07-05', True)
        self.assert_at('x-2018-07-06', '2018-07-06', False)
        self.assert_at('x-2018-07-06', '2018-07-07', False)
        # numbered locations with start of range
        self.assert_at('x[1,2,3]2018-07-06-', '2018-07-05', False)
        self.assert_at('x[1,2,3]2018-07-06-', '2018-07-06', True)
        self.assert_at('x[1,2,3]2018-07-06-', '2018-07-07', True)
        self.assert_at('x[1,2,3]2018-07-06-', '2018-07-08', True)
        self.assert_at('x[1,2,3]2018-07-06-', '2018-07-09', False)
        # named locations with start of range
        self.assert_at('x[fri]2018-07-06-', '2018-07-05', False)
        self.assert_at('x[fri]2018-07-06-', '2018-07-06', True)
        self.assert_at('x[fri]2018-07-06-', '2018-07-07', False)
        # named locations with no range
        self.assert_at('x[fri]', '2018-07-05', False)
        self.assert_at('x[fri]', '2018-07-06', True)
        self.assert_at('x[fri]', '2018-07-07', False)
        s = Schedule('x')
        self.assertEqual(s.start_of_frame('2018-01-02'), to_date('1970-01-02'))
        self.assertEqual(s.start, None)
        self.assertEqual(s.finish, None)
        # this is not None because it is used to set end dates for repeating intervals
        self.assertEqual(s.next_frame('2018-01-02'), POS_INFINITY)

    def test_error_messages(self):
        with self.assertRaisesRegex(Exception, r'Cannot parse "z"'):
            Schedule('z')
        with self.assertRaisesRegex(Exception, r'Cannot parse "z2018-10-07-"'):
            Schedule('z2018-10-07-')
        with self.assertRaisesRegex(Exception, r'Numbered locations in daily frames not supported'):
            Schedule('d[1mon]')
        with self.assertRaisesRegex(Exception, r'Repetition and offset not supported by extended frames'):
            Schedule('2x')

    def test_describe(self):
        self.assertEqual(Schedule('d').describe(), 'Day')
        self.assertEqual(Schedule('m').describe(), 'Month')
        self.assertEqual(Schedule('y').describe(), 'Year')
        self.assertEqual(Schedule('x').describe(), 'All')
        self.assertEqual(Schedule('x[fri]2018-07-06-').describe(), 'Extended[fri]')
