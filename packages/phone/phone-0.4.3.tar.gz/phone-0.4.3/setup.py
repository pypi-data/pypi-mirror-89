# coding:utf-8
from setuptools import setup,find_packages

PACKAGE = "phone"
NAME = "phone"
DESCRIPTION = "手机号码库"
AUTHOR = "ls0f"
AUTHOR_EMAIL = "admin@lovedboy.com"
URL = "https://github.com/ls0f/phone"
VERSION = '0.4.3'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    include_package_data = True,
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    zip_safe=False,
)
