import datetime
import json
import os


class FileManager:
    def __init__(self, backup_dir, offline_dir):
        os.makedirs(backup_dir, exist_ok=True)
        os.makedirs(offline_dir, exist_ok=True)
        self.backupDir = backup_dir
        self.offlineDir = offline_dir

    def user_file_exists(self, username):
        user_file = os.path.join(self.offlineDir, f"{username}.json")
        return os.path.exists(user_file)

    def read_data(self, username):
        user_file = os.path.join(self.offlineDir, f"{username}.json")
        if os.path.exists(user_file):
            with open(user_file, 'r') as file:
                data = json.load(file)
                return data
        raise FileNotFoundError(f"User file {user_file} not found")

    def write_data(self, username, data):
        user_file = os.path.join(self.offlineDir, f"{username}.json")
        with open(user_file, 'w') as file:
            json.dump(data, file, indent=2)

    def make_backup(self, username):
        backup_file = os.path.join(self.backupDir, f"{username}_backup.json")
        data = self.read_data(username)
        with open(backup_file, 'w') as file:
            json.dump(data, file, indent=2)
