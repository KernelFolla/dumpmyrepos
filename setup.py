# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


def get_version():
    with open('dumpmyrepos/__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def get_install_requires():
    ret = []
    with open('requirements.txt') as f:
        for line in f:
            ret.append(line)
    try:
        import argparse
    except ImportError:
        ret.append('argparse')
    return ret


setup(
    name='dumpmyrepos',
    version=get_version(),
    url='https://github.com/kernelfolla/dumpmyrepos',
    license='mit',
    author='Marino Di Clemente',
    author_email='kernelfolla@gmail.com',
    description='This python script will backup all your git repos',
    long_description='This python script will backup all your git repos using ssh locally, supports github gitlab'
                     + 'and bitbucket. All settings are passed using a config.yml file',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['config.yml']},
    install_requires=get_install_requires(),
    entry_points={
        'console_scripts': [
            'dumpmyrepos = dumpmyrepos.cli:main'
        ]
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: System :: Systems Administration',
        'Programming Language :: Python',
    ],
)
