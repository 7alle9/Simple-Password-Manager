import datetime

import cryptomodule as crypto
import filemodule as files
import dbmodule as db
from configmodule import appConfig
import os
from logmodule import Logger


def time_now():
    return datetime.datetime.now().timestamp()


logger = Logger(appConfig['logFile'], 'Manager')

class Manager:
    def __init__(self):
        self.isAuth = False
        self.username = None
        self.masterPassword = None

    def __auth(self, username, password):
        credentials = {'username': username, 'password': password}
        is_success, message = db.login(credentials)

        if not is_success:
            raise Exception(message)

        self.username = username
        self.masterPassword = password
        self.isAuth = True

    def __fetch_data_package(self):
        if not self.isAuth:
            raise Exception('Not authenticated')

        credentials = {'username': self.username, 'password': self.masterPassword}
        is_success, result = db.get_user_data(credentials)

        if not is_success:
            raise Exception(result)

        return result

    def login(self, username, password):
        self.__auth(username, password)

        data_package = self.__fetch_data_package()
        self.encryptedKeys = data_package['keys']
        self.encryptedPasswords = data_package['values']
        self.decryptedKeys = crypto.decrypt_list(self.masterPassword, self.encryptedKeys)
        self.decryptedPasswords = crypto.decrypt_dict(self.masterPassword, self.encryptedPasswords)



manager = Manager()
manager.execute_build_sequence('7alle9', '123456')
print(manager.add_password('facebook', '123'))
