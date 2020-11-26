from logging import StreamHandler, LogRecord


class LogHandler(StreamHandler):
    def __init__(self, print_func):
        StreamHandler.__init__(self)
        self.print_func = print_func

    def emit(self, record: LogRecord) -> None:
        self.print_func(record.message)
