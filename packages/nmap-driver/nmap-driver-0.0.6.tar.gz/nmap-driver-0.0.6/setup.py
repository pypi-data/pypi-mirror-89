#!/usr/bin/env python
# -*- coding:utf-8 -*-


from setuptools import setup, find_packages

setup(
    name = 'nmap-driver',
    version = '0.0.6',
    keywords='wx',
    description = 'a library for nmap scan',
    license = 'MIT License',
    url = 'https://192.168.1.146:8081/repo/packages',
    author = 'superman',
    author_email = '646390966@qq.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [
'exception==0.1.0',
'grpcio==1.32.0',
'ipdb==0.13.4',
'pid==3.0.4',
'protobuf==3.13.0',
'python-daemon==2.2.4',
'python-nmap==0.6.1',
'configparser==5.0.1'
]
)
