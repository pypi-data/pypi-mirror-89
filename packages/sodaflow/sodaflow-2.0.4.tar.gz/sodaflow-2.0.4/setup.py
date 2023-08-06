# setup.py
from setuptools import setup, find_packages


setup(
    name='sodaflow',
    version='2.0.4',
    author='agilesoda',
    author_email='agilesoda@gmail.com',
    description='Greet someone',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "soda-nni = cli.main:main"
        ]
    },
    install_requires=['click',
                      'requests']
)
