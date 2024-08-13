import datetime
import os


def get_now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')


class Logger:
    def __init__(self, log_dir):
        os.makedirs(log_dir, exist_ok=True)
        self.logFile = os.path.join(log_dir, 'logs.txt')

    def log(self, text, is_error=False):
        state = 'error' if is_error else 'info'
        log_text = f"[{get_now()}][{state}]: {text}\n"
        open(self.logFile, 'a').write(log_text)
        # print(log_text)
