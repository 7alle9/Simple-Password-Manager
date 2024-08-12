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


def make_backup(data, directory):
    now = int(datetime.datetime.now().timestamp())
    os.makedirs(directory, exist_ok=True)
    backup_file = os.path.join(directory, f"backup{now}.json")
    write_data(backup_file, data)
