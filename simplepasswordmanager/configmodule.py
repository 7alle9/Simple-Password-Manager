from platformdirs import user_data_dir, user_log_dir, user_config_dir
import configparser
import os

config = configparser.ConfigParser()

configDir = user_config_dir("spm")
os.makedirs(configDir, exist_ok=True)
configFilePath = os.path.join(configDir, "config.ini")

print(configFilePath)
if os.path.exists(configFilePath):
    config.read(configFilePath)
else:
    config['UserData'] = {
        'backupsDir': os.path.join(user_data_dir("spm"), "backups"),
        'offlineFile': os.path.join(user_data_dir("spm"), "offline.json")
    }
    config['App'] = {
        'logFile': os.path.join(user_log_dir("spm"), ".log"),
        'isOnline': True
    }
    with open(configFilePath, "w") as configFile:
        config.write(configFile)

appConfig = {
    'backupsDir': config['UserData']['backupsDir'],
    'offlineFile': config['UserData']['offlineFile'],
    'logFile': config['App']['logFile'],
    'isOnline': config['App'].getboolean('isOnline')
}