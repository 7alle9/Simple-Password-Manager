Simple Password Manager
=======================

Overview
--------
Simple Password Manager is a lightweight and secure Python package for managing passwords. It allows users to store, retrieve, and manage their passwords securely using encryption with a single master password. It supports two types of storage: local storage and cloud storage. The package provides a command-line interface (CLI) for easy management of passwords.

Features
--------
- **Encryption:** All passwords are encrypted using a master password.
- **Secure Storage:** Passwords are stored in a secure format locally or in the cloud.
- **Command-Line Interface:** Easy to use CLI for managing passwords.
- **Custom Password Generation:** Generate secure passwords on the fly.
- **Log and Backup System:** Keeps track of changes and allows for easy backup.

Installation
------------
Install the package using pip:

.. code-block:: bash

    pip install simple-password-manager

Usage
-----

**Command-Line Interface (CLI)**

The Simple Password Manager can be used directly from the command line with the following commands:

1. **Start in Online or Offline Mode:**

   - For online use, where your passwords are stored securely in the cloud:

     .. code-block:: bash

         spm mode -o

   - For offline use, where your passwords are stored locally:

     .. code-block:: bash

         spm mode -f

2. **Create an Account:**
   - Once the mode is selected, sign up by creating an account:

     .. code-block:: bash

         spm signup <username>

3. **Manage Your Passwords:**
   - After creating an account, you can begin managing your passwords with the following commands:
     - **Add a new password:**

       .. code-block:: bash

           spm add <service> <username>

     - **Retrieve a password:**

       .. code-block:: bash

           spm get <service>

     - **Update an existing password:**

       .. code-block:: bash

           spm update <service>

     - **Delete a password:**

       .. code-block:: bash

           spm delete <service>

   - There are options to view keys, change master password, and change the current user.

**Python Integration**

You can also use Simple Password Manager directly in your Python code:

.. code-block:: python

    from simplepasswordmanager import Manager, OfflineManager

    # Initialize the manager
    manager = Manager()

    # Example usage:
    manager.login("username", "masterpassword")
    manager.add_password("service", "password")
    print(manager.get_password("service"))

Notes
-----
If you have your own solution to store your passwords on the cloud, you can modify where the package stores your passwords online by updating the settings in `setting.py`.
