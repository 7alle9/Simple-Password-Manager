from platformdirs import user_data_dir, user_log_dir, user_config_dir
import configparser
import os

config = configparser.ConfigParser()

configDir = user_config_dir("spm")
os.makedirs(configDir, exist_ok=True)
configFilePath = os.path.join(configDir, "config.ini")

if os.path.exists(configFilePath):
    config.read(configFilePath)
else:
    config['UserData'] = {
        'backupDir': os.path.join(user_data_dir("spm"), "backups"),
        'offlineDir': os.path.join(user_data_dir("spm"), "offline")
    }
    config['App'] = {
        'logDir': user_log_dir("spm"),
        'isOnline': True
    }
    with open(configFilePath, "w") as configFile:
        config.write(configFile)

appConfig = {
    'backupDir': config['UserData']['backupDir'],
    'offlineDir': config['UserData']['offlineDir'],
    'logDir': config['App']['logDir'],
    'isOnline': config['App'].getboolean('isOnline')
}

# print(appConfig)