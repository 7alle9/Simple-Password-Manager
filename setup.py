from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A simple password manager'
LONG_DESCRIPTION = 'A manager that stores your passwords securely and allows you to manage them'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
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
    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)