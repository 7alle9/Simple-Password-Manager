from setuptools import setup, find_packages


def get_readme():
    with open('README.rst', 'r') as f:
        return f.read()


VERSION = '0.0.3'
DESCRIPTION = 'A simple password manager'
LONG_DESCRIPTION = get_readme()

setup(
    name="simple-password-manager",
    version=VERSION,
    author="Amir Mallek",
    author_email="mallekamir123@gmail.com",
    url="https://github.com/7alle9/Simple-Password-Manager",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
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
