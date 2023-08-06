import logging
from contextlib import contextmanager
from contextvars import ContextVar
from copy import deepcopy


class ContextFilter(logging.Filter):
    """ Should support threads and asyncio """

    def __init__(self):
        self.stack = ContextVar("logging_context", default=[])

    def filter(self, record):
        for name, data in self.stack.get():
            setattr(record, name, data)
        return True

    def enter(self, name, data):
        if not name:
            raise ValueError("Name for context filter must be provided")
        if not data:
            raise ValueError("Data for context filter must be provided")
        state = deepcopy(self.stack.get())
        state.append((name, deepcopy(data)))
        self.stack.set(state)

    def exit(self):
        state = deepcopy(self.stack.get())
        state.pop()
        self.stack.set(state)


context_filter = ContextFilter()


@contextmanager
def Context(name, data):
    context_filter.enter(name, data)
    yield None
    context_filter.exit()
