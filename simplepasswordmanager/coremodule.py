import datetime

import cryptomodule as crypto
import filemodule as files
import dbmodule as db
from configmodule import appConfig
import os
from logmodule import Logger


def time_now():
    return datetime.datetime.now().timestamp()


logger = Logger(appConfig['logDir'])


class Manager:
    def __init__(self):
        self.isAuth = False
        self.username = None
        self.masterPassword = None

    def __auth(self, username, password):
        logger.log(f"-Authenticating user {username}-")

        logger.log('Checking with server')
        credentials = {'username': username, 'password': password}
        is_success, message = db.login(credentials)

        if not is_success:
            logger.log(f"Failed to authenticate user {username}: {message}", is_error=True)
            raise Exception(message)

        logger.log(f"-User {username} authenticated-")
        self.username = username
        self.masterPassword = password
        self.isAuth = True

    def __fetch_data_package(self):
        logger.log('-Fetching data package-')

        if not self.isAuth:
            logger.log('Not authenticated user', is_error=True)
            raise Exception('Not authenticated')

        logger.log('Fetching data from server')
        credentials = {'username': self.username, 'password': self.masterPassword}
        is_success, result = db.get_user_data(credentials)

        if not is_success:
            logger.log(f"Failed to fetch data package: {result}", is_error=True)
            raise Exception(result)

        logger.log('-Data package fetched-')
        return result

    def login(self, username, password):
        logger.log('-Logging in-')

        self.__auth(username, password)

        data_package = self.__fetch_data_package()

        logger.log('Unpacking and Decrypting data package')
        self.encryptedKeys = data_package['keys']
        self.encryptedPasswords = data_package['values']
        self.decryptedKeys = crypto.decrypt_list(self.masterPassword, self.encryptedKeys)
        self.decryptedPasswords = crypto.decrypt_dict(self.masterPassword, self.encryptedPasswords)

        logger.log('-Login successful and manager ready-')

    def get_password(self, key):
        key = key.upper()
        logger.log(f"-Getting password for key '{key}'-")

        if not self.isAuth:
            logger.log('Not authenticated user', is_error=True)
            raise Exception('Not authenticated')

        if key not in self.decryptedKeys:
            logger.log(f"Key '{key}' not found", is_error=True)
            raise Exception('Key not found')

        logger.log(f"-Password for key '{key}' retrieved-")
        return self.decryptedPasswords[key]

    def add_password(self, key, password):
        key = key.upper()
        logger.log(f"-Adding password for key '{key}'-")

        if not self.isAuth:
            logger.log('Not authenticated user', is_error=True)
            raise Exception('Not authenticated')

        if key in self.decryptedKeys:
            logger.log(f"Key '{key}' already exists", is_error=True)
            raise Exception('Key already exists')

        logger.log('Adding key and password to data')
        self.decryptedKeys.append(key)
        self.decryptedPasswords[key] = password
        encrypted_key = crypto.encrypt_string(self.masterPassword, key)
        encrypted_password = crypto.encrypt_string(self.masterPassword, password)
        self.encryptedKeys.append(encrypted_key)
        self.encryptedPasswords[key] = encrypted_password

        logger.log('Updating data package on server')
        credentials = {'username': self.username, 'password': self.masterPassword}
        is_success, message = db.add_new_password(credentials, encrypted_key, encrypted_password)

        if not is_success:
            logger.log(f"Failed to add password: {message}", is_error=True)
            raise Exception(message)

        logger.log(f"-Password for key '{key}' added-")


test = Manager()
test.login('Amir', '123456')
