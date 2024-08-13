import argparse
from .cliconfig import set_username, get_username, set_mode, get_mode
from .coremodule import OfflineManager, OnlineManager
import getpass

parser = argparse.ArgumentParser(description="A Simple Password Manager Command Line Interface")
subparsers = parser.add_subparsers(title='Commands', help='Command help', dest='command')

# get password
getParser = subparsers.add_parser('get', help='Get a password', description='Get a password for a given key',
                                  usage='spm get <key>')
getParser.add_argument('key', help='The key for the password')

# add password
addParser = subparsers.add_parser('add', help='Add a new password', description='Add password for a new key',
                                  usage='''
                        spm add <key> <password>
                        or spm add <key> -a [-l <length]''')
addParser.add_argument('key', help='The key for the password')
addParser.add_argument('password', help='The password to store', nargs='?')
addParser.add_argument('-a', '--auto-genrate', action='store_true', help='Auto genrate a new password')
addParser.add_argument('-l', '--length', type=int,
                       help='The length of the password to genrate(Default is 16)', default=16)

# update password
updateParser = subparsers.add_parser('update', help='Update a password',
                                     description='Update a password of an exisiting key')
updateParser.add_argument('key', help='The key for the password')
updateParser.add_argument('password', help='The new password', nargs='?')
updateParser.add_argument('-a', '--auto-genrate', action='store_true', help='Auto genrate a new password')
updateParser.add_argument('-l', '--length', type=int,
                          help='The length of the password to genrate(Default is 16)', default=16)

# delete password
deleteParser = subparsers.add_parser('delete', help='Delete a password', description='Delete a password for a given key')
deleteParser.add_argument('key', help='The key for the password')

# username specification
userParser = subparsers.add_parser('user', help='Get or set the username', description='Get or set the username')
userGroup = userParser.add_mutually_exclusive_group()
userGroup.add_argument('-s', '--set', help='Set the username')

# manager mode
modeParser = subparsers.add_parser('mode', help='Get or change manager mode',
                                   description='Specifies manager mode either online or offline')
modeGroup = modeParser.add_mutually_exclusive_group()
modeGroup.add_argument('-o', '--online', action='store_true', help='Set manager mode to online')
modeGroup.add_argument('-f', '--offline', action='store_true', help='Set manager mode to offline')

args = parser.parse_args()


def login():
    if not username:
        raise parser.error('Username not set. Use "spm user -s <username>" to set username')
    master_password = getpass.getpass('Enter Master Password: ')
    manager.login(username, master_password)


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
            print(f"Username: {username}")
        else:
            print('Username not set. Use "spm user -s <username>" to set username')


username = get_username()
managerMode = get_mode()
manager = OfflineManager() if managerMode == 'offline' else OnlineManager()
match args.command:
    case 'mode':
        mode()
    case 'user':
        user()
    case 'get' | 'add' | 'update' | 'delete':
        login()
        match args.command:
            case 'get':
                print(manager.get_password(args.key))
            case 'add':
                print('Add password')
            case 'update':
                print('Update password')
            case 'delete':
                print('Delete password')
            case None:
                parser.print_help()
    case _:
        raise parser.error('Invalid command')