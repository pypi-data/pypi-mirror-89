from django.apps import AppConfig
from django.db.models.signals import pre_save, pre_delete

from simple_trigger_audit import signals
from simple_trigger_audit.utils import get_trigger_audit_models


class SimpleTriggerAuditAppConfig(AppConfig):
    name = "simple_trigger_audit"

    def ready(self):
        # TODO: we shouldn't connect signals if middleware is not configured
        for app_config in self.apps.get_app_configs():
            trigger_audit_models = get_trigger_audit_models(app_config) or []

            for model_class_name in trigger_audit_models:
                model_class = app_config.get_model(model_class_name)
                pre_save.connect(signals.django_simple_trigger_request_info, sender=model_class)
                pre_delete.connect(signals.django_simple_trigger_request_info, sender=model_class)
