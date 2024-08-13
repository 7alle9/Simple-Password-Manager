import datetime
from . import cryptomodule as crypto
from . import dbmodule as db
from .configmodule import appConfig
from .logmodule import Logger
from .filemodule import FileManager


def now_str():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')


logger = Logger(appConfig['logDir'])


class Manager:
    def login(self, username, password):
        pass

    def signup(self, username, password):
        pass

    def get_keys(self):
        pass

    def get_password(self, key):
        pass

    def add_password(self, key, password, auto_generate=False, length=16):
        pass

    def update_password(self, key, password, auto_generate=False, length=16):
        pass

    def delete_password(self, key):
        pass

    def change_master_password(self, new_password):
        pass


class OnlineManager(Manager):
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
            if message == 'User does not exist':
                logger.log(f"User {username} does not exist", is_error=True)
                raise AccountNotFoundException(message)
            logger.log(f"Failed to authenticate user {username}: {message}", is_error=True)
            raise BadCredentialsException(message)

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

    def signup(self, username, password):
        logger.log('-Signing up-')

        logger.log('Checking with server')
        credentials = {
            'username': username,
            'password': crypto.hash_password(password)
        }
        is_success, message = db.signup(credentials)

        if not is_success:
            logger.log(f"Failed to signup user {username}: {message}", is_error=True)
            raise UserAlreadyExistsException(message)

        logger.log('-Signup successful-')
        self.login(username, password)

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
            raise KeyNotFoundException('Key not found')

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
            raise KeyAlreadyExistsException('Key already exists')

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
            raise KeyNotFoundException('Key not found')

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


class OfflineManager(Manager):
    def __init__(self):
        self.isAuth = False
        self.username = None
        self.masterPassword = None
        self.userData = None
        self.fileManager = FileManager(appConfig['backupDir'], appConfig['offlineDir'])

    def __auth(self, username, password):
        logger.log(f"-Authenticating user {username}-")

        logger.log('Checking with local data')
        hashed_username = crypto.hash_password(username)
        try:
            self.user_data = self.fileManager.read_data(hashed_username)
        except FileNotFoundError:
            logger.log(f"User {username} does not exist", is_error=True)
            raise AccountNotFoundException('User does not exist')

        hashed_password = crypto.hash_password(password)
        if hashed_password == self.user_data['password']:
            logger.log(f"-User {username} authenticated-")
            self.username = username
            self.masterPassword = password
            self.isAuth = True
            return

        logger.log(f"Failed to authenticate user {username}", is_error=True)
        raise BadCredentialsException('Authentication failed')

    def __update_data_package(self):
        logger.log('-Updating data package-')

        hashed_username = crypto.hash_password(self.username)
        hashed_password = crypto.hash_password(self.masterPassword)

        logger.log(f"Making backup for user {self.username}")
        self.fileManager.make_backup(hashed_username)

        if not self.isAuth:
            logger.log('Not authenticated user', is_error=True)
            raise Exception('Not authenticated')

        logger.log('Updating local data')
        self.user_data['keys'] = self.keys
        self.user_data['values'] = self.encryptedPasswords
        self.user_data['lastUpdate'] = self.updateHistory
        self.user_data['password'] = hashed_password
        self.fileManager.write_data(hashed_username, self.user_data)

        logger.log('-Data package updated-')

    def login(self, username, password):
        logger.log('-Logging in-')

        self.__auth(username, password)

        logger.log('Unpacking and decrypting data')
        self.keys = self.user_data['keys']
        self.encryptedPasswords = self.user_data['values']
        self.decryptedPasswords = crypto.decrypt_dict(self.masterPassword, self.encryptedPasswords)
        self.updateHistory = self.user_data['lastUpdate']

        logger.log('-Login successful and manager ready-')

    def signup(self, username, password):
        logger.log('-Signing up-')

        logger.log('Checking with local data')
        hashed_username = crypto.hash_password(username)
        if self.fileManager.user_file_exists(hashed_username):
            logger.log(f"User {username} already exists", is_error=True)
            raise UserAlreadyExistsException('User already exists')

        logger.log('Creating new user data')
        hashed_password = crypto.hash_password(password)
        self.user_data = {
            'keys': [],
            'values': {},
            'password': hashed_password,
            'lastUpdate': {}
        }
        self.fileManager.write_data(hashed_username, self.user_data)

        logger.log('-Signup successful-')
        self.login(username, password)

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
            raise KeyNotFoundException('Key not found')

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
            raise KeyAlreadyExistsException('Key already exists')

        logger.log('Generating strong password')
        if auto_generate:
            password = crypto.generate_strong_password(length)

        logger.log('Adding key and password to data')
        encrypted_password = crypto.encrypt_string(self.masterPassword, password)
        self.keys.append(key)
        self.decryptedPasswords[key] = password
        self.encryptedPasswords[key] = encrypted_password
        self.updateHistory[key] = now_str()

        self.__update_data_package()

        logger.log(f"-Password for key '{key}' added-")

    def update_password(self, key, password, auto_generate=False, length=16):
        key = key.upper()
        logger.log(f"-update password for key '{key}'-")

        if not self.isAuth:
            logger.log('Not authenticated user', is_error=True)
            raise Exception('Not authenticated')

        if key not in self.keys:
            logger.log(f"Key '{key}' not found", is_error=True)
            raise KeyNotFoundException('Key not found')

        logger.log('Generating strong password')
        if auto_generate:
            password = crypto.generate_strong_password(length)

        logger.log('Editing key and password in data')
        encrypted_password = crypto.encrypt_string(self.masterPassword, password)
        self.decryptedPasswords[key] = password
        self.encryptedPasswords[key] = encrypted_password
        self.updateHistory[key] = now_str()

        self.__update_data_package()

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
        del self.updateHistory[key]

        self.__update_data_package()

        logger.log(f"-Password for key '{key}' deleted-")

    def change_master_password(self, new_password):
        logger.log('-Changing master password-')

        if not self.isAuth:
            logger.log('Not authenticated user', is_error=True)
            raise Exception('Not authenticated')

        logger.log('Encrypting data with new password')
        self.encryptedPasswords = crypto.encrypt_dict(new_password, self.decryptedPasswords)
        self.masterPassword = new_password

        logger.log('Updating data')
        self.__update_data_package()

        logger.log('-Master password changed-')


class KeyNotFoundException(Exception):
    def __init__(self, message):
        self.message = message


class KeyAlreadyExistsException(Exception):
    def __init__(self, message):
        self.message = message


class BadCredentialsException(Exception):
    def __init__(self, message):
        self.message = message


class AccountNotFoundException(BadCredentialsException):
    def __init__(self, message):
        self.message = message


class UserAlreadyExistsException(Exception):
    def __init__(self, message):
        self.message = message