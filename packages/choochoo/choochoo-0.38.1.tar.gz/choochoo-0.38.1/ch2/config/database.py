from json import dumps
from logging import getLogger

from sqlalchemy import desc

from ..names import simple_name
from ..common.names import TIME_ZERO
from ..sql import ActivityGroup, Constant, Pipeline, PipelineType, StatisticName, StatisticJournalType, \
    DiaryTopic, DiaryTopicField, ActivityTopic, ActivityTopicField
from ..sql.tables.constant import ValidateNamedTuple
from ..sql.types import long_cls, short_cls

log = getLogger(__name__)

NEARBY_CNAME = 'nearby'


class Counter:

    def __init__(self, start=10, delta=10):
        self.__start = start
        self.__delta = delta
        self.__previous = None

    def __call__(self, reset=None, delta=None):
        if delta is not None:
            if delta < 1:
                raise Exception('Negative increment')
            self.__delta = delta
        if reset is None:
            if self.__previous is None:
                self.__previous = self.__start
            else:
                self.__previous += self.__delta
        else:
            if reset <= self.__previous:
                raise Exception('Sort not increasing with reset')
            else:
                self.__previous = reset
        return self.__previous


def add(s, instance):
    '''
    Add an instance to the session (and so to the database), returning the instance.
    You likely don't need this - see the more specific helpers below.

    The instance can of any class that subclasses the Field class from SQLAlchemy.
    In practice, that means most classes in the ch2.sql.tables module.
    However, only some classes make sense in the context of a configuration, and
    more specific helpers probably already exist for those.
    '''
    s.add(instance)
    return instance


def add_activity_group(s, title, sort, description=None):
    '''
    Add an activity type to the configuration.

    These are used to group activities (and related statistics).
    So typical entries might be for cycling, running, etc.
    '''
    return add(s, ActivityGroup(name=title, sort=sort, description=description))


def add_pipeline(s, cls, type, blocked_by=None, **kargs):
    pipeline = add(s, Pipeline(cls=cls, type=type, kargs=kargs))
    for blocker in blocked_by or ():
        if isinstance(blocker, Pipeline):
            log.debug(f'{short_cls(blocker.cls)} blocks {short_cls(cls)}')
            pipeline.blocked_by.append(blocker)
        else:
            q = s.query(Pipeline). \
                filter(Pipeline.type == pipeline.type,
                       Pipeline.cls == blocker)
            if q.count():
                for instance in q.all():
                    pipeline.blocked_by.append(instance)
                log.debug(f'{blocker} blocks {cls}')
            else:
                raise Exception(f'{short_cls(blocker)} is not a current pipeline')
    return pipeline


def add_next_pipeline(s, cls, type, **kargs):
    previous = s.query(Pipeline).filter(Pipeline.type == type).order_by(desc(Pipeline.id)).first()
    if previous: previous = [previous]
    return add_pipeline(s, cls, type, blocked_by=previous, **kargs)


def add_displayer(s, cls, **kargs):
    '''
    Add a class to the diary pipeline.

    The pipeline classes are invoked when the diary is displayed.
    They generate display classes for activity statistics (and similar)

    The sort argument fixes the order in which the classes are instantiated and called and can
    be an integer or a callable (that returns an integer) like Counter above.

    The kargs are passed to the constructor and so can be used to customize the processing.
    '''
    log.debug(f'Adding displayer pipeline {short_cls(cls)}')
    return add_next_pipeline(s, cls, PipelineType.DISPLAY, **kargs)


def add_activity_displayer_delegate(s, cls, **kargs):
    '''
    Add a class to the activity displayer pipeline.

    The pipeline classes are invoked when the diary is displayed, for each activity.

    The sort argument fixes the order in which the classes are instantiated and called and can
    be an integer or a callable (that returns an integer) like Counter above.

    The kargs are passed to the constructor and so can be used to customize the processing.
    '''
    log.debug(f'Adding activity displayer pipeline {short_cls(cls)}')
    return add_next_pipeline(s, cls, PipelineType.DISPLAY_ACTIVITY, **kargs)


def add_process(s, cls, blocked_by=None, **kargs):
    '''
    Add a class to the process pipeline.

    The pipeline classes are invoked when activities are imported from FIT files.
    They read the files and create journal entries and associated statistics.

    The blocked_by argument fixes the order in which the classes are instantiated and called and can
    be an integer or a callable (that returns an integer) like Counter above.

    The kargs are passed to the constructor and so can be used to customize the processing.
    '''
    log.debug(f'Adding process pipeline {short_cls(cls)}')
    return add_pipeline(s, cls, PipelineType.PROCESS, blocked_by=blocked_by, **kargs)


def add_constant(s, title, value, description=None, units=None, name=None,
                 statistic_journal_type=StatisticJournalType.INTEGER, activity_group=None,
                 time=TIME_ZERO, single=False, validate_cls=None, validate_args=None, validate_kargs=None):
    '''
    Add a constant.

    Configuring a constant allows the user to supply a value later, using the `ch2 constant` command.
    This can be useful for values that don't vary often, and so aren't worth adding to the diary.
    An example is FTHR, which you will only measure occasionally, but which is needed when calculating
    activity statistics (also, FTHR can vary by activity, which is why we add a constant per activity).
    '''
    if name is None: name = simple_name(title)
    log.debug(f'Adding constant {name}')
    statistic_name = StatisticName.add_if_missing(s, name, statistic_journal_type, units, None, Constant,
                                                  title=title, description=description)
    activity_group = ActivityGroup.from_name(s, activity_group)
    constant = add(s, Constant(statistic_name=statistic_name,
                               name=statistic_name.qualified_name(s, activity_group),
                               activity_group=activity_group, single=single, validate_cls=validate_cls,
                               validate_args=validate_args, validate_kargs=validate_kargs))
    if value:
        constant.add_value(s, value, time=time)
    else:
        log.warning(f'No value for constant {name}')
    return constant


def add_enum_constant(s, title, enum, value, description=None, units=None, single=False, name=None,
                      activity_group=None, time=0.0):
    '''
    Add a constant that is a JSON encoded enum.  This is validated before saving.
    '''
    return add_constant(s, title, dumps(value), description=description, units=units, name=name,
                        statistic_journal_type=StatisticJournalType.TEXT, activity_group=activity_group,
                        time=time, single=single, validate_cls=ValidateNamedTuple,
                        validate_args=[], validate_kargs={'tuple_cls': long_cls(enum)})


def set_constant(s, constant, value, time=None, date=None):
    '''
    Set a constant value.
    '''
    constant.add_value(s, value, time=time, date=date)


def add_diary_topic(s, title, sort, description=None, schedule=None):
    '''
    Add a root topic.

    DiaryTopics are displayed in the diary.
    They can be permanent, or associated with some schedule.
    They can also be associated with fields (and so with statistics).

    A root topic is usually used as a header to group related children.
    For example, 'DailyDiary' to group diary entries (notes, weight, sleep etc), or 'Plan' to group training plans.
    '''
    return add(s, DiaryTopic(title=title, sort=sort, description=description, schedule=schedule))


def add_child_diary_topic(s, parent, name, sort, description=None, schedule=None):
    '''
    Add a child topic.

    DiaryTopics are displayed in the diary.
    They can be permanent, or associated with some schedule.
    They can also be associated with fields (and so with statistics).

    A child topic is used to add additional structure to an existing topic.
    For example, the parent topic might be "injuries" and permanent, while children are defined for
    specific injuries with a schedule that gives start and end dates.
    '''
    return add(s, DiaryTopic(parent=parent, title=name, sort=sort, description=description, schedule=schedule))


def add_diary_topic_field(s, diary_topic, name, sort, type, description=None, units=None, summary=None, schedule=None,
                          model=None):
    '''
    Add a field and associated statistic to a topic entry.

    This is how the user can enter values into the diary.
    The field describes how the values are displayed in the diary.
    The statistic describes how the values are stored in the database.
    '''
    if diary_topic.id is None:
        s.flush()
    statistic_name = add(s, StatisticName(name=name, owner=DiaryTopic, statistic_journal_type=type,
                                          description=description, units=units, summary=summary))
    if model is None: model = {}
    field = add(s, DiaryTopicField(diary_topic=diary_topic, sort=sort, model=model, schedule=schedule,
                                   statistic_name=statistic_name))


def add_activity_topic(s, title, sort, description=None, activity_group=None):
    '''
    Add a root topic.

    DiaryTopics are displayed in the diary.
    They can be permanent, or associated with some schedule.
    They can also be associated with fields (and so with statistics).

    A root topic is usually used as a header to group related children.
    For example, 'DailyDiary' to group diary entries (notes, weight, sleep etc), or 'Plan' to group training plans.
    '''
    return add(s, ActivityTopic(title=title, sort=sort, description=description,
                                activity_group=ActivityGroup.from_name(s, activity_group)))


def add_child_activity_topic(s, parent, title, sort, description=None):
    '''
    Add a child topic.

    DiaryTopics are displayed in the diary.
    They can be permanent, or associated with some schedule.
    They can also be associated with fields (and so with statistics).

    A child topic is used to add additional structure to an existing topic.
    For example, the parent topic might be "injuries" and permanent, while children are defined for
    specific injuries with a schedule that gives start and end dates.
    '''
    return add(s, ActivityTopic(parent=parent, title=title, sort=sort, description=description))


def add_activity_topic_field(s, activity_topic, title, sort, type, activity_group,
                             description=None, units=None, summary=None, model=None):
    '''
    Add a field and associated statistic to a topic entry.

    This is how the user can enter values into the diary.
    The field describes how the values are displayed in the diary.
    The statistic describes how the values are stored in the database.
    '''
    if activity_topic and activity_topic.id is None:
        s.flush()
    # cannot simply add as this is also called during loading
    statistic_name = StatisticName.add_if_missing(s, title, type, units, summary, ActivityTopic,
                                                  description=description)
    if model is None: model = {}
    return add(s, ActivityTopicField(activity_topic=activity_topic, sort=sort, model=model,
                                     statistic_name=statistic_name))

