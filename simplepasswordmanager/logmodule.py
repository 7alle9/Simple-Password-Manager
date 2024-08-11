import datetime


def log(text):
    open('logs.txt', 'a').write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [info]: {text}\n")
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\033[{'34;1'}m{'[info]: '}\033[{'0'}m{text}")
