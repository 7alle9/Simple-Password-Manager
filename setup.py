from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A simple password manager'
LONG_DESCRIPTION = 'A manager that stores your passwords securely and allows you to manage them'

setup(
    name="simplepasswordmanager",
    version=VERSION,
    author="Amir Mallek",
    author_email="mallekamir123@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'cryptography',
        'requests',
        'platformdirs',
        'pyperclip'
    ],
    entry_points={
        'console_scripts': [
            'spm=simplepasswordmanager.cli:main',
        ],
    },
    keywords=['python', 'password', 'manager', 'simple', 'cli', 'security'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ]
)
