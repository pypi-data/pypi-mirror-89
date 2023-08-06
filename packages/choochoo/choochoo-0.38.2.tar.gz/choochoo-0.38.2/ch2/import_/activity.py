
from logging import getLogger

from . import journal_imported, match_statistic_name, copy_statistic_journal, any_attr
from ..common.log import log_current_exception
from ..sql import ActivityTopicJournal, FileHash, ActivityTopic, ActivityGroup
from ..names import simple_name

log = getLogger(__name__)


def import_activity(record, old, new):
    if not activity_imported(record, new):
        record.info('Importing activity entries')
        copied = set()  # avoid calling for multiple activity groups (doesn't cause duplicates but prints warnings)
        with old.session_context() as old_s:
            copy_activity_topic_fields(record, old_s, old, None, new, copied)
            activity_topic = old.meta.tables['activity_topic']
            for old_activity_topic in old_s.query(activity_topic).filter(activity_topic.c.parent_id == None).all():
                log.info(f'Found old (root) activity_topic {old_activity_topic}')
                copy_activity_topic_fields(record, old_s, old, old_activity_topic, new, copied)
    else:
        record.warning('Activity entries already imported')


def activity_imported(record, new):
    return journal_imported(record, new, ActivityTopicJournal, 'Activity')


def copy_activity_topic_fields(record, old_s, old, old_activity_topic, new, copied):
    log.debug(f'Trying to copy activity_topic_fields for activity_topic {old_activity_topic}')
    activity_topic_field = old.meta.tables['activity_topic_field']
    for old_activity_topic_field in old_s.query(activity_topic_field). \
            filter(activity_topic_field.c.activity_topic_id ==
                   (old_activity_topic.id if old_activity_topic else None)).all():
        log.debug(f'Found old activity_topic_field {old_activity_topic_field}')
        try:
            statistic_name = old.meta.tables['statistic_name']
            if statistic_name not in copied:
                old_statistic_name = old_s.query(statistic_name). \
                    filter(statistic_name.c.id == old_activity_topic_field.statistic_name_id).one()
                log.debug(f'Found old statistic_name {old_statistic_name}')
                with new.session_context() as new_s:
                    new_statistic_name = match_statistic_name(record, old_statistic_name, new_s, ActivityTopic)
                    copy_activity_topic_journal_entries(record, old_s, old, old_statistic_name, new_s,
                                                        new_statistic_name)
                copied.add(statistic_name)
        except:
            log_current_exception()
    if old_activity_topic:
        parent_id = old_activity_topic.id
        activity_topic = old.meta.tables['activity_topic']
        for old_activity_topic in old_s.query(activity_topic).filter(activity_topic.c.parent_id == parent_id).all():
            log.info(f'Found old activity_topic {old_activity_topic}')
            copy_activity_topic_fields(record, old_s, old, old_activity_topic, new)


def copy_activity_topic_journal_entries(record, old_s, old, old_statistic_name, new_s, new_statistic_name):
    log.debug(f'Trying to find statistic_journal entries for {old_statistic_name}')
    statistic_journal = old.meta.tables['statistic_journal']
    activity_topic_journal = old.meta.tables['activity_topic_journal']
    for old_statistic_journal in old_s.query(statistic_journal). \
            join(activity_topic_journal, statistic_journal.c.source_id == activity_topic_journal.c.id). \
            filter(statistic_journal.c.statistic_name_id == old_statistic_name.id).all():
        log.debug(f'Found old statistic_journal {old_statistic_journal}')
        old_activity_topic_journal = old_s.query(activity_topic_journal). \
            filter(activity_topic_journal.c.id == old_statistic_journal.source_id).one()
        log.debug(f'Found old activity_topic_journal {old_activity_topic_journal}')
        new_activity_topic_journal = create_activity_topic_journal(record, old_s, old, old_activity_topic_journal,
                                                                   old_statistic_name, new_s)
        copy_statistic_journal(record, old_s, old, old_statistic_name, old_statistic_journal,
                               new_s, new_statistic_name, new_activity_topic_journal)


def create_activity_topic_journal(record, old_s, old, old_activity_topic_journal, old_statistic_name, new_s):
    log.debug(f'Trying to create activity_topic_journal')
    file_hash = old.meta.tables['file_hash']
    old_file_hash = old_s.query(file_hash). \
        filter(file_hash.c.id == old_activity_topic_journal.file_hash_id).one()
    log.debug(f'Found old file_hash {old_file_hash}')
    # column name change 0-29 - 0-30 ?
    new_file_hash = FileHash.get_or_add(new_s, any_attr(old_file_hash, 'hash', 'md5'))
    log.debug(f'Found new file_hash {new_file_hash}')
    activity_group = old.meta.tables['activity_group']
    source = old.meta.tables['source']
    try:
        # new style both
        old_activity_group = old_s.query(activity_group). \
            join(source, source.c.activity_group_id == activity_group.c.id). \
            filter(source.c.id == old_activity_topic_journal.id).one()
    except:
        try:
            # old style, group associated with statistics
            old_activity_group = old_s.query(activity_group). \
                filter(activity_group.c.id == old_statistic_name.activity_group_id).one()
        except:
            # old / new style (0-33), group associated with source
            old_activity_group = old_s.query(activity_group). \
                filter(activity_group.c.id == old_activity_topic_journal.activity_group_id).one()
    log.debug(f'Found old activity_group {old_activity_group}')
    new_activity_group = new_s.query(ActivityGroup). \
        filter(ActivityGroup.name == simple_name(old_activity_group.name)).one()
    log.debug(f'Found new activity_group {new_activity_group}')
    new_activity_topic_journal = ActivityTopicJournal.get_or_add(new_s, new_file_hash, new_activity_group)
    log.debug(f'Found new activity_topic_journal {new_activity_topic_journal}')
    return new_activity_topic_journal
