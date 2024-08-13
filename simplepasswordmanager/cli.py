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
addParser.add_argument('-a', '--auto-genrate', action='store_true', help='Auto genrate a new password')
addParser.add_argument(
    '-l', '--length',
    type=int,
    help='The length of the password to genrate(Default is 16)',
    default=16
)

# update password
updateParser = subparsers.add_parser(
    'update',
    help='Update a password',
    description='Update a password of an exisiting key',
    usage='''\n   spm update <key> <password>\nor spm update <key> -a [-l LENGTH]'''
)
updateParser.add_argument('key', help='The key for the password')
updateParser.add_argument('password', help='The new password', nargs='?')
updateParser.add_argument('-a', '--auto-genrate', action='store_true', help='Auto genrate a new password')
updateParser.add_argument(
    '-l', '--length',
    type=int,
    help='The length of the password to genrate(Default is 16)',
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

# change master password
changeParser = subparsers.add_parser(
    'change',
    help='Change the master password',
    description='Change the master password',
    usage='spm change'
)

# signup
signupParser = subparsers.add_parser(
    'sign',
    help='Create a new account',
    description='Create a new account with a unique username and a master password',
    usage='spm sign <username>'
)
signupParser.add_argument('username', help='The username for the account')

args = parser.parse_args()


def login():
    if not username:
        raise parser.error('Username not set. Use "spm user -s <username>" to set username')
    master_password = getpass.getpass('Enter Master Password: ')
    try:
        manager.login(username, master_password)
    except BadCredentialsException:
        print('Invalid username or password')
        print('Use "spm sign <username>" to create a new account')
        exit()


def mode():
    if args.online:
        set_mode('online')
        print('Mode set to online')
    elif args.offline:
        set_mode('offline')
        print('Mode set to offline')
    else:
        print(f"Manager mode: {managerMode}")


def user():
    if args.set:
        set_username(args.set)
        print(f"Username set to {args.set}")
    else:
        if username:
            print(username)
        else:
            print('Username not set.')
            print('   use "spm user -s <username>" to set username')
            print('or use "spm sign <username>" to create a new account')


def get():
    login()
    try:
        password = manager.get_password(args.key)
        if args.copy:
            pyperclip.copy(password)
            print(f'Password copied to clipboard')
        else:
            print(password)
    except KeyNotFoundException:
        print(f"key '{args.key}' not found")


def add():
    login()
    try:
        if args.auto_genrate:
            manager.add_password(args.key, '', auto_generate=True, length=args.length)
        else:
            new_password = getpass.getpass(f"Enter the password for '{args.key}': ")
            manager.add_password(args.key, new_password)
        print(f"Password added")
    except KeyAlreadyExistsException:
        print(f"key '{args.key}' already exists \n Use 'spm update' to update the password")


def update():
    login()
    try:
        if args.auto_genrate:
            manager.update_password(args.key, '', auto_generate=True, length=args.length)
        else:
            manager.update_password(args.key, args.password)
        print(f"Password updated")
    except KeyNotFoundException:
        print(f"key '{args.key}' not found")


def delete():
    login()
    manager.delete_password(args.key)
    print(f"Password deleted")


def keys():
    login()
    print('Keys:')
    if not manager.get_keys():
        print('No keys stored')
    for key in manager.get_keys():
        print(key)


def change():
    login()
    new_password = getpass.getpass('Enter new Master Password: ')
    manager.change_master_password(new_password)
    print('Master Password changed')


def signup():
    master_password = getpass.getpass('Enter Master Password: ')
    confirm_password = getpass.getpass('Confirm Master Password: ')
    if master_password != confirm_password:
        print('Passwords do not match')
        exit()
    try:
        manager.signup(args.username, master_password)
    except UserAlreadyExistsException:
        print('Username already exists')
        exit()

    global username
    username = args.username
    set_username(username)
    print('Account created')


username = get_username()
managerMode = get_mode()
manager: Manager = OfflineManager() if managerMode == 'offline' else OnlineManager()
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
    case 'change':
        change()
    case 'sign':
        signup()
    case _:
        raise parser.error('Invalid command. Use "spm -h" for help')
