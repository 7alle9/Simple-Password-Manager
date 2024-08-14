# Simple Password Manager
[![PyPI version](https://badge.fury.io/py/simple-password-manager.svg)](https://badge.fury.io/py/simple-password-manager)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Overview
Simple Password Manager is a lightweight and secure Python package for managing passwords. It allows users to store, retrieve, and manage their passwords securely using encryption with a single master password. It supports two types of storage: local storage and cloud storage. The package provides a command-line interface (CLI) for easy management of passwords.

## Features
- **Encryption:** All passwords are encrypted using a master password.
- **Secure Storage:** Passwords are stored in a secure format locally or in the cloud.
- **Command-Line Interface:** Easy to use CLI for managing passwords.
- **Custom Password Generation:** Generate secure passwords on the fly.
- **Log and Backup System:** Keeps track of changes and allows for easy backup.

## Installation
Install the package using pip:

```bash
pip install simple-password-manager
```

## Usage

### Command-Line Interface (CLI)
The Simple Password Manager can be used directly from the command line with the following commands:

1. **Start in Online or Offline Mode:**
   - For online use, where your passwords are stored securely in the cloud:
     ```bash
     spm mode -o
     ```
   - For offline use, where your passwords are stored locally:
     ```bash
     spm mode -f
     ```

2. **Create an Account:**
   - Once the mode is selected, sign up by creating an account:
     ```bash
     spm signup <username>
     ```

3. **Manage Your Passwords:**
   - After creating an account, you can begin managing your passwords with the following commands:
     - **Add a new password:**
       ```bash
       spm add <service> <username>
       ```
     - **Retrieve a password:**
       ```bash
       spm get <service>
       ```
     - **Update an existing password:**
       ```bash
       spm update <service>
       ```
     - **Delete a password:**
       ```bash
       spm delete <service>
       ```

### Python Integration
You can also use Simple Password Manager directly in your Python code:

```python
from simplepasswordmanager import Manager, OfflineManager, OnlineManager

# Initialize the manager
manager = Manager(master_password="your_master_password")

# Example usage:
manager.add_password("gmail", "your_email@gmail.com", "your_password")
password = manager.get_password("gmail")
print(f"Retrieved password: {password}")
```

## Notes
- If you have your own solution to store your passwords on the cloud, you can modify where the package stores your passwords online by updating the settings in setting.py.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.