#dumpmyrepos

## Description

This python script will backup all of your git repos using ssh locally, supports github gitlab and bitbucket.
All settings are passed using a config.yml file

## Installation

as first install the script with pip

```bash
pip install --user https://github.com/kernelfolla/dumpmyrepos/archive/master.zip
```
now create a config.yml file

```bash
dumpmyrepos --make-config=config.yml
```
finally run the script

```bash
dumpmyrepos --config=config.yml
```
or read all available options

```bash
dumpmyrepos --help
```

## Authentication

services Github, Gitlab and Bitbucket supports authentication via a private token or a key/secret (bitbucket), my suggestion is to use this way instead of username/password because you can always remove these keys from yur panel, or change password without breaking your backup settings. Anyway username/password authentication is supported for all 3 services  

## Requirements

You do need to have your ssh keys uploaded for the computer that you are running the backup on.

## License

dumpmyrepos is a "Marino Di Clemente" open source project, distributed under the MIT license.
