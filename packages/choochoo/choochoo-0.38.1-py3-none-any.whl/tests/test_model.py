from logging import getLogger
from tempfile import TemporaryDirectory

from ch2.commands.args import DEV, V, BASE, bootstrap_db, UPLOAD
from ch2.commands.upload import upload
from ch2.common.args import mm, m
from ch2.config.profiles.default import default
from ch2.diary.database import read_date
from ch2.diary.model import LABEL, VALUE
from ch2.lib import to_date
from tests import LogTestCase, random_test_user

log = getLogger(__name__)


class TestModel(LogTestCase):

    def test_constant(self):
        user = random_test_user()
        with TemporaryDirectory() as f:
            bootstrap_db(user, mm(BASE), f, m(V), '5', mm(DEV), configurator=default)
            config = bootstrap_db(user, mm(BASE), f, mm(DEV), UPLOAD,
                                  'data/test/source/personal/2018-03-04-qdp.fit', '-K', 'n_cpu=1')
            upload(config)
            with config.db.session_context() as s:
                model = list(read_date(s, to_date('2018-03-04')))
                for i, x in enumerate(model):
                    print(i, x)
                [title, diary, shrimp, activity, database] = model
                activity = activity[1][3]  # multiple now supported
                print(activity)
                name = activity[1]
                print(name)
                self.assertEqual(name[LABEL], 'Name')
                self.assertEqual(name[VALUE], '2018-03-04T07:16:33')
                route = activity[3]
                print(route)
                self.assertEqual(route[LABEL], 'Route')
