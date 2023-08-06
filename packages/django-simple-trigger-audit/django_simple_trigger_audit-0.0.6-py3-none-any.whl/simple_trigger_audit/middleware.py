import threading

__all__ = [
    "get_current_request",
    "get_written_flag",
    "set_written_flag",
    "get_current_request_trace_id",
]

import uuid


def get_current_request():
    return getattr(_thread_locals, 'request', None)


def get_written_flag():
    return getattr(_thread_locals, 'written_flag', None)


def set_written_flag(written_flag):
    _thread_locals.written_flag = written_flag


def get_current_request_trace_id():
    return getattr(_thread_locals, 'trace_id', None)


#
# Private API
#

_thread_locals = threading.local()


def _set_current_request(request):
    _thread_locals.request = request


def _set_current_request_trace_id(trace_id):
    _thread_locals.trace_id = trace_id


class TriggerAuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_written_flag(False)
        _set_current_request(request)
        _set_current_request_trace_id(str(uuid.uuid4()))
        try:
            response = self.get_response(request)
        except:  # noqa
            raise
        finally:
            set_written_flag(None)
            _set_current_request(None)
            _set_current_request_trace_id(None)
        return response
