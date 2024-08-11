from cryptomodule import *
from filemodule import *
import os


class Manager:
    filePath = "C:\\Users\\amirm\\PycharmProjects\\password-manager\\passwords.json"
    # toDelete password=haha
    testKey = 'TEST'
    expected = 'haha'

    def __init__(self):
        log('----Initializing Manager----')
        log('Reading encrypted data')
        self.encryptedData = read_data(Manager.filePath)
        self.decryptedData = {}
        self.isAuth = False
        self.masterPassword = None

    def authenticate(self, password):
        try:
            log('Authenticating')
            test = self.encryptedData[Manager.testKey]
            testee = decrypt_string(password, test)
            if testee == Manager.expected:
                log('Successfull Authentication')
                self.isAuth = True
                self.masterPassword = password
                log('Decrypting data')
                self.decryptedData = decrypt_data(self.masterPassword, self.encryptedData)
                return True
            log('Failed Authentication')
        except Exception as e:
            log('Failed Authentication')
            print(e)
            return False

    def check_password(self, password):
        log('Checking password')
        if self.isAuth:
            return self.masterPassword == password
        return False

    def get_password(self, key):
        key = key.upper()
        log(f"Getting password for '{key}'")
        if self.isAuth and self.decryptedData.keys().__contains__(key):
            return self.decryptedData[key]
        return None

    def modify_password(self, key, password):
        log(f"Making encryted backup in '{os.getcwd()}'")
        make_backup(self.encryptedData)
        self.decryptedData[key] = password
        self.encryptedData[key] = encrypt_string(self.masterPassword, password)
        log('Writing new encryted data')
        write_data(Manager.filePath, self.encryptedData)

    def add_password(self, key, password):
        key = key.upper()
        if self.isAuth and not self.decryptedData.keys().__contains__(key):
            log(f"Adding password for '{key}'")
            self.modify_password(key, password)
            return True
        return False

    def update_password(self, key, password):
        key = key.upper()
        if self.isAuth and self.decryptedData.keys().__contains__(key):
            log(f"Updating password for '{key}'")
            self.modify_password(key, password)
            return True
        return False

    def change_master_password(self, new_password):
        log('Changing Master Password')
        log(f"Making encrypted backup in '{os.getcwd()}'")
        make_backup(self.encryptedData)
        log('Encrypting data with new password')
        self.encryptedData = encrypt_data(new_password, self.decryptedData)
        log('Writing new encrypted data')
        write_data(Manager.filePath, self.encryptedData)
        self.masterPassword = new_password
        log('Master Password Updated')

    @staticmethod
    def generate_password():
        log('Generating password')
        return generate_strong_password()
