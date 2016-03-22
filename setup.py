# coding: utf-8
from setuptools import setup

setup(
    name='postino',
    version='0.1',
    description='Easy email sending',
    url='http://github.com/mlesniew/postino',
    author='Michał Leśniewski',
    author_email='mlesniew@gmail.com',
    license='GPLv3',
    packages=['postino'],
    install_requires=[
        'markdown',
        'pyzmail',
    ],
    scripts=['bin/postino'],
    zip_safe=False)
