import json
import logging

from django.db import models
from django.db.models import Model

import simple_trigger_audit.signals  # noqa

logger = logging.getLogger(__name__)


class TriggerAuditEntry(Model):
    """
    This instances are created by the trigger. This exists to facilitate querying.
    """
    object_table = models.CharField(max_length=128)
    object_pk = models.IntegerField()
    object_payload = models.TextField()

    audit_entry_created = models.DateTimeField(auto_now_add=True)
    audit_txid_current = models.BigIntegerField()
    audit_operation = models.CharField(max_length=32)
    audit_version = models.IntegerField()
    audit_request_info = models.TextField()

    class Meta:
        managed = False
        db_table = "trigger_audit_entries_v1"

    def __str__(self):
        return f"{self.__class__.__name__} " \
               f"{self.object_table}[{self.object_pk}] " \
               f"{self.audit_operation}"

    @property
    def object_payload_json(self) -> dict:
        return json.loads(self.object_payload)

    def is_insert(self):
        return self.audit_operation == 'INSERT'

    def is_update(self):
        return self.audit_operation == 'UPDATE'

    def is_delete(self):
        return self.audit_operation == 'DELETE'
