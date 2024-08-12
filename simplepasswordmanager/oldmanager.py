class Manager:
    def __init__(self):
        self.isAuth = False
        self.username = None
        self.masterPassword = None

    def execute_build_sequence(self, username, password):
        log('Executing build sequence')
        self.authenticate_online(username, password)
        fresh_package = self.get_fresh_package()
        log('Making Encrypted copy offline')
        files.write_data(appConfig['offlineFile'], fresh_package)
        self.extract_encrypted_components(fresh_package)
        self.decrypt_components()
        log('Build sequence complete')

    def authenticate_online(self, username, password):
        log(f"Attempting to authenticate '{username}' online")
        credentials = {'username': username, 'password': password}
        if db.login(credentials):
            log('Online authentication successful')
            self.username = '7alle9'
            self.masterPassword = '123456'
            self.isAuth = True
            return
        log('Online authentication failed')
        raise Exception('Online authentication failed')

    def get_fresh_package(self):
        log('Attempting to get fresh data')
        if not self.isAuth:
            log('User not authenticated')
            raise Exception('Not authenticated')
        credentials = {'username': self.username, 'password': self.masterPassword}
        data = db.get_user_data(credentials)
        log('Fresh data retrieved')
        return data

    def extract_encrypted_components(self, data):
        log('Extracting encrypted data')
        self.encryptedKeys = data['keys']
        self.encryptedData= data['values']
        self.encyptedLastUpdate = data['lastUpdate']

    def decrypt_components(self):
        log('Attempting to decrypt data')
        if not self.isAuth:
            log('User not authenticated')
            raise Exception('Not authenticated')
        log('Decrypting key list')
        self.decryptedKeys = decrypt_list(self.masterPassword, self.encryptedKeys)
        log('Decrypting password data')
        self.decryptedData = decrypt_data(self.masterPassword, self.encryptedData)

    def get_password(self, key):
        log(f"Attempting to get password for '{key}'")
        if not self.isAuth:
            log('User not authenticated')
            raise Exception('Not Authenticated')
        key = key.upper()
        if self.decryptedKeys.__contains__(key):
            log(f"Password for '{key}' found")
            return self.decryptedData[key]
        log(f"Password for '{key}' not found")
        raise Exception('Key not found')

    def get_encrypted_package(self):
        log('Attempting to get encrypted package')
        if not self.isAuth:
            log('User not authenticated')
            raise Exception('Not Authenticated')

        log('Creating encypted package')
        package = {
            'keys': self.encryptedKeys,
            'values': self.encryptedData,
            'lastUpdate': self.encyptedLastUpdate
        }
        return package

    def update_data_offline(self, key, password):
        log(f"Attempt to update data for '{key}'")
        if not self.isAuth:
            log('User not authenticated')
            raise Exception('Not Authenticated')
        key = key.upper()
        log(f"Making encryted backup in '{appConfig['backupsDir']}'")
        files.make_backup(self.encryptedData, appConfig['backupsDir'])
        log('Updating data')
        self.decryptedData[key] = password
        encrypted_key = encrypt_string(self.masterPassword, key)
        self.encryptedData[encrypted_key] = encrypt_string(self.masterPassword, password)
        self.encyptedLastUpdate[encrypted_key] = time_now()
        log('Writing new encryted data')
        files.write_data(appConfig['offlineFile'], self.get_encrypted_package())

    def add_password(self, key, password):
        log(f"Attempting to add password for '{key}'")
        if not self.isAuth:
            log('User not authenticated')
            raise Exception('Not Authenticated')
        key = key.upper()
        if not self.decryptedData.keys().__contains__(key):
            log(f"Adding password for '{key}' offline")
            self.decryptedKeys.append(key)
            encrypted_key = encrypt_string(self.masterPassword, key)
            self.encryptedKeys.append(encrypted_key)
            self.update_data_offline(key, password)
            log(f"Adding password for '{key}' online")

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