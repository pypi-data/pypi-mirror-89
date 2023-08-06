import logging

from django.apps import AppConfig
from django.db import connections
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from simple_trigger_audit import middleware
from simple_trigger_audit.utils import get_trigger_audit_models


logger = logging.getLogger(__name__)


trigger_audit_entry_creator_trigger_tmpl = """
-- https://www.postgresql.org/message-id/1360944248465-5745434.post%40n5.nabble.com
DO 
$src$
BEGIN
IF NOT EXISTS(SELECT * FROM information_schema.triggers
              WHERE event_object_table = '{table_name}' AND trigger_name = '{trigger_name}') 
    THEN

        CREATE TRIGGER {trigger_name}
            AFTER INSERT OR UPDATE OR DELETE ON {table_name}
            FOR EACH ROW EXECUTE FUNCTION trigger_audit_entry_creator_func_v1();

    END IF;
END;
$src$
"""


@receiver(post_migrate)
def audit_run_post_migrate(app_config: AppConfig, verbosity, using, **kwargs):
    # TODO: add 'untracked_tables' to AppConfig so we can automatically delete old triggers

    # Django 3.0: emit_post_migrate_signal emited by *flush*, only includes SOME of the documented parameters
    # plan = kwargs.get('plan')
    # apps = kwargs.get('apps')

    trigger_audit_models = get_trigger_audit_models(app_config)
    if trigger_audit_models is None:
        if verbosity >= 2:
            print(f"Ignored: no 'trigger_audit_models' found in app_config {app_config}")
        return

    if not trigger_audit_models:
        if verbosity >= 2:
            print(f"Empty 'trigger_audit_models' found in app_config {app_config}")
        return

    with connections[using].cursor() as cursor:
        # For now we use the 'using' connection we received. Not sure if that's the best approach.
        if verbosity >= 2:
            print("Running 'trigger_audit_entry_creator_trigger_tmpl'")
        for model_class_name in trigger_audit_models:
            model_class = app_config.get_model(model_class_name)
            if verbosity >= 1:
                print(f" - Creating trigger on table '{model_class._meta.db_table}'")

            sql = trigger_audit_entry_creator_trigger_tmpl.format(
                table_name=model_class._meta.db_table,
                trigger_name='trigger_audit_entry_creator_trigger',
            )
            if verbosity >= 3:
                print(f"SQL: {sql}")

            result = cursor.execute(sql)

            if verbosity >= 3:
                print(f"cursor.execute(sql) result: {result}")
            # FIXME: check result


# *****************************************************************************
# About original implementation of signal handler
# *****************************************************************************
# trigger_audit_entry_creator_trigger_tmpl = """
# -- This looks dangerous, but seems to be the recommended approach.
# -- Nevertheless, it looks dangerous, and if for some reason a CASCADE DROP
# --  happens (it should't, but anyway), so, better try some other alternative
# BEGIN;
# DROP TRIGGER IF EXISTS trigger_audit_entry_creator_trigger ON {table_name};
# CREATE TRIGGER trigger_audit_entry_creator_trigger
#     AFTER INSERT OR UPDATE OR DELETE ON {table_name}
#     FOR EACH ROW EXECUTE FUNCTION trigger_audit_entry_creator_func();
#
# COMMIT;
# """
# *****************************************************************************


django_simple_trigger_request_info_sql = """
select set_config('django_simple_trigger.request_info', %s || ',' || %s, true);
"""


def django_simple_trigger_request_info(sender, **kwargs):
    request = middleware.get_current_request()
    if request is None:
        logger.warning("django_simple_trigger_request_info(): middleware.get_current_request() returned None")
        return

    # TODO: maybe we shouldn't bother to write `request_info` if user is anonymous
    # if not request.user.is_authenticated:
    #     return

    if middleware.get_written_flag():
        logger.debug("django_simple_trigger_request_info(): request_info already set")
        return

    trace_id = middleware.get_current_request_trace_id()
    user_id = request.user.pk if request.user.is_authenticated else 0
    logger.debug("django_simple_trigger_request_info(): trace_id=%s user_id=%s", trace_id, user_id)
    with connections["default"].cursor() as cursor:
        cursor.execute(django_simple_trigger_request_info_sql, [
            str(trace_id),
            str(user_id),
        ])
    middleware.set_written_flag(True)
