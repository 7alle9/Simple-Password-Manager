from logmodule import log
import datetime
import json
import os


def read_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data


def write_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def make_backup(data, directory='backups'):
    if not os.path.exists(directory):
        os.makedirs(directory)
        log(f"Backup Directory {directory} created")

    now = int(datetime.datetime.now().timestamp())
    write_data(f"{directory}/backup{now}.json", data)
