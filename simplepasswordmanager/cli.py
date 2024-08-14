import argparse
import pyperclip
from simplepasswordmanager.cliconfig import set_username, get_username, set_mode, get_mode
from simplepasswordmanager.coremodule import *
import getpass

parser = argparse.ArgumentParser(description="A Simple Password Manager Command Line Interface")
subparsers = parser.add_subparsers(title='Commands', help='Command help', dest='command')

# get password
getParser = subparsers.add_parser(
    'get',
    help='Get a password',
    description='Get a password for a given key',
    usage='spm get <key>'
)
getParser.add_argument('key', help='The key for the password')
getParser.add_argument('-c', '--copy', action='store_true', help='Copy the password to clipboard without displaying it')

# add password
addParser = subparsers.add_parser(
    'add',
    help='Add a new password',
    description='Add password for a new key',
    usage='spm add <key> [-a] [-l LENGTH]'
)
addParser.add_argument('key', help='The key for the password')
addParser.add_argument('-a', '--auto-generate', action='store_true', help='Auto generate a new password')
addParser.add_argument(
    '-l', '--length',
    type=int,
    help='The length of the password to generate(Default is 16)',
    default=16
)

# update password
updateParser = subparsers.add_parser(
    'update',
    help='Update a password',
    description='Update a password of an existing key',
    usage='''\n   spm update <key> <password>\nor spm update <key> -a [-l LENGTH]'''
)
updateParser.add_argument('key', help='The key for the password')
updateParser.add_argument('password', help='The new password', nargs='?')
updateParser.add_argument('-a', '--auto-generate', action='store_true', help='Auto generate a new password')
updateParser.add_argument(
    '-l', '--length',
    type=int,
    help='The length of the password to generate(Default is 16)',
    default=16
)

# delete password
deleteParser = subparsers.add_parser(
    'delete',
    help='Delete a password',
    description='Delete a password for a given key',
    usage='spm delete <key>'
)
deleteParser.add_argument('key', help='The key for the password')

# username specification
userParser = subparsers.add_parser(
    'user',
    help='Get or set the username',
    description='Get or set the username',
    usage='spm user [-s USERNAME]'
)
userParser.add_argument('-s', '--set', help='Set the username')

# manager mode
modeParser = subparsers.add_parser(
    'mode',
    help='Get or change manager mode',
    description='Specifies manager mode either online or offline',
    usage='spm mode [-o | -f]'
)
modeGroup = modeParser.add_mutually_exclusive_group()
modeGroup.add_argument('-o', '--online', action='store_true', help='Set manager mode to online')
modeGroup.add_argument('-f', '--offline', action='store_true', help='Set manager mode to offline')

# get keys
getKeysParser = subparsers.add_parser(
    'keys',
    help='Get all keys',
    description='Get all keys managed by spm',
    usage='spm keys'
)
getKeysParser.add_argument('-l', '--long', action='store_true', help='Display keys and the last time they were updated')

# change master password
masterParser = subparsers.add_parser(
    'master',
    help='Change the master password',
    description='Change the master password',
    usage='spm master'
)

# signup
signupParser = subparsers.add_parser(
    'signup',
    help='Create a new account',
    description='Create a new account with a unique username and a master password',
    usage='spm signup <username>'
)
signupParser.add_argument('username', help='The username for the account')

args = parser.parse_args()


def login():
    if not username:
        raise parser.error('Username not set. Use "spm user -s <username>" to set username')
    master_password = getpass.getpass('Enter Master Password: ')
    try:
        manager.login(username, master_password)
    except UserDoesNotExistException:
        print('User does not exist')
        print('Use "spm signup <username>" to create a new account', end='')
        exit()
    except BadCredentialsException:
        print('   Check username or password maybe incorrect')
        print('or use "spm sign <username>" to create a new account', end='')
        exit()


def mode():
    if args.online:
        set_mode('online')
        print('Mode set to online', end='')
    elif args.offline:
        set_mode('offline')
        print('Mode set to offline', end='')
    else:
        print(f"Manager mode: {managerMode}", end='')


def user():
    if args.set:
        set_username(args.set)
        print(f"Username set to {args.set}", end='')
    else:
        if username:
            print(username)
        else:
            print('Username not set.')
            print('   use "spm user -s <username>" to set username')
            print('or use "spm sign <username>" to create a new account', end='')


def get():
    login()
    try:
        password = manager.get_password(args.key)
        if args.copy:
            pyperclip.copy(password)
            print(f'Password copied to clipboard', end='')
        else:
            print(password)
    except KeyNotFoundException:
        print(f"key '{args.key}' not found", end='')


def add():
    login()
    try:
        if args.auto_generate:
            manager.add_password(args.key, '', auto_generate=True, length=args.length)
        else:
            new_password = getpass.getpass(f"Enter the password for '{args.key}': ")
            manager.add_password(args.key, new_password)
        print(f"Password added", end='')
    except KeyAlreadyExistsException:
        print(f"key '{args.key}' already exists")
        print("Use 'spm update' to update the password", end='')


def update():
    login()
    try:
        if args.auto_generate:
            manager.update_password(args.key, '', auto_generate=True, length=args.length)
        else:
            manager.update_password(args.key, args.password)
        print(f"Password updated", end='')
    except KeyNotFoundException:
        print(f"key '{args.key}' not found", end='')


def delete():
    login()
    manager.delete_password(args.key)
    print(f"Password deleted", end='')


def keys():
    login()
    if not manager.get_keys():
        print('No keys stored', end='')

    keys_len = len(manager.get_keys())

    if args.long:
        history = manager.get_history()
        for i in range(keys_len):
            key = manager.get_keys()[i]
            if i == keys_len - 1:
                print(f'{key} - {history[key]}', end='')
            else:
                print(f'{key} - {history[key]}')
    else:
        for i in range(keys_len):
            key = manager.get_keys()[i]
            if i == keys_len - 1:
                print(key, end='')
            else:
                print(key)


def master():
    login()
    new_password = getpass.getpass('Enter new Master Password: ')
    manager.change_master_password(new_password)
    print('Master Password changed', end='')


def signup():
    master_password = getpass.getpass('Enter Master Password: ')
    confirm_password = getpass.getpass('Confirm Master Password: ')
    if master_password != confirm_password:
        print('Passwords do not match', end='')
        exit()
    try:
        manager.signup(args.username, master_password)
    except UserAlreadyExistsException:
        print('Username already exists', end='')
        exit()

    global username
    username = args.username
    set_username(username)
    print('Account created', end='')


username = get_username()
managerMode = get_mode()
manager: Manager = OfflineManager() if managerMode == 'offline' else OnlineManager()


def main():
    match args.command:
        case 'mode':
            mode()
        case 'user':
            user()
        case 'get':
            get()
        case 'add':
            add()
        case 'update':
            update()
        case 'delete':
            delete()
        case 'keys':
            keys()
        case 'master':
            master()
        case 'signup':
            signup()
        case _:
            raise parser.error('Invalid command. Use "spm -h" for help')


if __name__ == "__main__":
    main()
