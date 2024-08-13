from platformdirs import user_data_dir, user_log_dir, user_config_dir
import configparser
import os


def update_config():
    with open(configFilePath, "w") as file:
        config.write(file)


def set_username(username):
    config['user']['username'] = username
    update_config()


def get_username():
    return config['user']['username'] if config['user'].__contains__('username') else None


def set_mode(mode):
    config['user']['mode'] = mode
    update_config()


def get_mode():
    return config['user']['mode']


config = configparser.ConfigParser()

configDir = user_config_dir("spm")
os.makedirs(configDir, exist_ok=True)
configFilePath = os.path.join(configDir, "cliconfig.ini")

if os.path.exists(configFilePath):
    config.read(configFilePath)
else:
    config['user'] = {'mode': 'offline'}
    update_config()
