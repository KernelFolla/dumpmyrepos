# !/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from shutil import copyfile

import yaml
import sys
from .config import Config


def main():
    parser = argparse.ArgumentParser(description="Usage: %prog [options] ")
    parser.add_argument("-c", "--config", dest="config_path", help="config.yml file location")
    parser.add_argument("-mc", "--make-config", dest="makeconfig", help="make a standard config.yml file")
    parser.add_argument("-d", "--dry-run", dest="dry_run", action="store_true", help="dry run")
    parser.add_argument("-q", "--quiet", dest="quiet", action="store_true", help="No output to stdout")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="Verbose output of all commands")
    parser.add_argument("-nd", "--no-dry-run", dest="dry_run", action="store_false", help="no dry run")
    parser.add_argument("-nq", "--no-quiet", dest="quiet", action="store_false", help="No output to stdout")
    parser.add_argument("-nv", "--no-verbose", dest="verbose", action="store_false",
                        help="No verbose output of all commands")

    parser.add_argument("-b", "--base_path", dest="base_path", help="Local backup location")
    parser.add_argument("-m", "--max-attempts", type=int, dest="max_attempts", help="Max attempts")
    parser.add_argument("-p", "--parallel-downloads", type=int, dest="parallel_downloads", help="Parallel downloads")
    parser.add_argument("-cc", "--cmd-clone", dest="cmd_clone", help="Command to clone the repo")
    parser.add_argument("-cu", "--cmd-update", dest="cmd_update", help="Command to update the repo")

    parser.set_defaults(quiet=None)
    parser.set_defaults(verbose=None)
    parser.set_defaults(dry_run=None)
    args = parser.parse_args()

    if args.makeconfig is not None:
        make_config(args.makeconfig)
        sys.exit(0)

    settings = load_settings(args)
    conf = Config(settings)
    conf.dump_all()


def load_settings(args):
    config_path = None
    try:
        config_path = args.config_path
        if not config_path:
            config_path = raw_input('Enter the path of your config.yml file: ')
        config_path = os.path.abspath(config_path)
    except KeyboardInterrupt:
        print "Caught KeyboardInterrupt, terminating"

    with open(config_path, 'r') as stream:
        try:
            settings = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    if 'command' not in settings:
        settings['command'] = {}
    if 'services' not in settings:
        settings['services'] = {}
    for key, value in vars(args).items():
        if not (value is None or key in ('makeconfig', 'config_path')):
            settings['command'][key] = value
    return settings


def make_config(dest):
    src = os.path.join(os.path.dirname(__file__), 'config.yml')
    copyfile(src, dest)


if __name__ == '__main__':
    main()
