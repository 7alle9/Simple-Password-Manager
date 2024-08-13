from setuptools import setup, find_packages

import os


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()


VERSION = '0.0.2'
DESCRIPTION = 'A simple password manager'
LONG_DESCRIPTION = read_file('README.md')

setup(
    name="simple-passwor-dmanager",
    version=VERSION,
    author="Amir Mallek",
    author_email="mallekamir123@gmail.com",
    url="https://github.com/7alle9/Simple-Password-Manager",
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
