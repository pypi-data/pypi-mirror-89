##!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='rngtool',
    version='0.5',
    author='Ayub Farah',
    author_email='razortyphon@gmail.com',
    description='Quick random number generating tool for Linux',
    packages=find_packages(),
    url='https://github.com/ayubf/rngtool',
    license='MIT',
    scripts=['bin/rngtool.py'],
    entry_points = {
        'console_scripts' : ['rngtool=rngtool:main']
    }
)