import datetime

import cryptomodule as crypto
import dbmodule as db
from configmodule import appConfig
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
        credentials = {
            'username': username,
            'password': crypto.hash_password(password)
        }
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
        is_success, result = db.get_user_data(self.__get_credentials())

        if not is_success:
            logger.log(f"Failed to fetch data package: {result}", is_error=True)
            raise Exception(result)

        logger.log('-Data package fetched-')
        return result

    def __get_credentials(self):
        logger.log('-Getting credentials-')

        if not self.isAuth:
            logger.log('Not authenticated user', is_error=True)
            raise Exception('Not authenticated')

        return {
            'username': self.username,
            'password': crypto.hash_password(self.masterPassword)
        }

    def refresh_data(self):
        logger.log('-Refreshing data-')

        if not self.isAuth:
            logger.log('Not authenticated user', is_error=True)
            raise Exception('Not authenticated')

        data_package = self.__fetch_data_package()

        logger.log('Unpacking and Decrypting data package')
        self.keys = data_package['keys']
        self.encryptedPasswords = data_package['values']
        self.decryptedPasswords = crypto.decrypt_dict(self.masterPassword, self.encryptedPasswords)

        logger.log('-Data refreshed-')

    def login(self, username, password):
        logger.log('-Logging in-')

        self.__auth(username, password)

        self.refresh_data()

        logger.log('-Login successful and manager ready-')

    def get_keys(self):
        logger.log('-Getting keys-')

        if not self.isAuth:
            logger.log('Not authenticated user', is_error=True)
            raise Exception('Not authenticated')

        logger.log('-Keys retrieved-')
        return self.keys

    def get_password(self, key):
        key = key.upper()
        logger.log(f"-Getting password for key '{key}'-")

        if not self.isAuth:
            logger.log('Not authenticated user', is_error=True)
            raise Exception('Not authenticated')

        if key not in self.keys:
            logger.log(f"Key '{key}' not found", is_error=True)
            raise Exception('Key not found')

        logger.log(f"-Password for key '{key}' retrieved-")
        return self.decryptedPasswords[key]

    def add_password(self, key, password, auto_generate=False, length=16):
        key = key.upper()
        logger.log(f"-Adding password for key '{key}'-")

        if not self.isAuth:
            logger.log('Not authenticated user', is_error=True)
            raise Exception('Not authenticated')

        if key in self.keys:
            logger.log(f"Key '{key}' already exists", is_error=True)
            raise Exception('Key already exists')

        logger.log('Generating strong password')
        if auto_generate:
            password = crypto.generate_strong_password(length)

        logger.log('Adding key and password to data')
        encrypted_password = crypto.encrypt_string(self.masterPassword, password)
        self.keys.append(key)
        self.decryptedPasswords[key] = password
        self.encryptedPasswords[key] = encrypted_password

        logger.log('Updating data package on server')
        is_success, message = db.add_new_password(self.__get_credentials(), key, encrypted_password)

        if not is_success:
            logger.log(f"Failed to add password: {message}", is_error=True)
            raise Exception(message)

        logger.log(f"-Password for key '{key}' added-")

    def update_password(self, key, password, auto_generate=False, length=16):
        key = key.upper()
        logger.log(f"-update password for key '{key}'-")

        if not self.isAuth:
            logger.log('Not authenticated user', is_error=True)
            raise Exception('Not authenticated')

        if key not in self.keys:
            logger.log(f"Key '{key}' not found", is_error=True)
            raise Exception('Key not found')

        logger.log('Generating strong password')
        if auto_generate:
            password = crypto.generate_strong_password(length)

        logger.log('Editing key and password in data')
        encrypted_password = crypto.encrypt_string(self.masterPassword, password)
        self.decryptedPasswords[key] = password
        self.encryptedPasswords[key] = encrypted_password

        logger.log('Updating data package on server')
        is_success, message = db.update_password(self.__get_credentials(), key, encrypted_password)

        if not is_success:
            logger.log(f"Failed to edit password: {message}", is_error=True)
            raise Exception(message)

        logger.log(f"-Password for key '{key}' updated-")

    def delete_password(self, key):
        key = key.upper()
        logger.log(f"-Deleting password for key '{key}'-")

        if not self.isAuth:
            logger.log('Not authenticated user', is_error=True)
            raise Exception('Not authenticated')

        if key not in self.keys:
            logger.log(f"-Key '{key}' not found-", is_error=True)
            return

        logger.log('Deleting key and password from data')
        self.keys.remove(key)
        del self.decryptedPasswords[key]
        del self.encryptedPasswords[key]

        logger.log('Updating data package on server')
        is_success, message = db.delete_password(self.__get_credentials(), key)

        if not is_success:
            logger.log(f"Failed to delete password: {message}", is_error=True)
            raise Exception(message)

        logger.log(f"-Password for key '{key}' deleted-")

    def change_master_password(self, new_password):
        logger.log('-Changing master password-')

        if not self.isAuth:
            logger.log('Not authenticated user', is_error=True)
            raise Exception('Not authenticated')

        self.refresh_data()

        logger.log('Encrypting data with new password')
        new_encrypted_passwords = crypto.encrypt_dict(new_password, self.decryptedPasswords)

        logger.log('Updating data package on server')
        is_success, message = db.change_master_password(self.__get_credentials(), new_password, new_encrypted_passwords)

        if not is_success:
            logger.log(f"Failed to change master password: {message}", is_error=True)
            raise Exception(message)

        self.masterPassword = new_password
        logger.log('-Master password changed-')


test = Manager()
test.login('Amir','123456')
# test.change_master_password('123456')
print(test.get_password('facebook'))
