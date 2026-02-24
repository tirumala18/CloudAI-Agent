from contextvars import ContextVar

current_account_id = ContextVar('current_account_id', default='default')