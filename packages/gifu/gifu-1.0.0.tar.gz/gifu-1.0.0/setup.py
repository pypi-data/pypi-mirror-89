#!/usr/bin/env python3
import os.path
from setuptools import setup

with open('README.rst', 'rb') as file:
    readme = file.read().decode('utf8')
    
setup(
    name='gifu',
    version='1.0.0',
    url='https://github.com/narutolavo/gifu',
    license='MIT License',
    author='Narutolavo',
    author_email='narutoolavo@outlook.com',
    keywords='traduzir, estudar, anki, ingles',
    description='Usando um programa para traduzir, e criando baralhos para o anki',
    long_description=readme,
    packages=['gifu'],
    install_requires=['googletrans==4.0.0rc1'],
     entry_points={
        'gui_scripts': [
            'gifu = gifu:__main__',
        ]
    },
    data_files=[('gifu', ['gifu/gifu.xbm', 'gifu/tekisuto.txt'])],
)
