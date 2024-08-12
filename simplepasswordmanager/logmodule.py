import datetime


def get_now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')


class Logger:
    def __init__(self, log_file, log_source):
        self.log_file = log_file
        self.log_source = log_source

    def log(self, text, is_error=False):
        state = 'error' if is_error else 'info'
        log_text = f"[{get_now()}][{self.log_source}][{state}]: {text}\n"
        open(self.log_file, 'a').write(log_text)

