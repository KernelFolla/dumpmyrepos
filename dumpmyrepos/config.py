# -*- coding: utf-8 -*-

from .services.factory import factory
from multiprocess import Pool
from command import Command
import itertools


class Config:
    def __init__(self, settings):
        self.settings = settings

    def get_accounts(self):
        services = self.settings['services']
        return map(lambda x: factory(x, services[x]), services)

    def get_repositories(self):
        accounts = self.get_accounts()
        pool = Pool(len(accounts))
        try:
            res = pool.map_async(lambda x: x.get_repositories(), accounts).get(999999)
            chain = itertools.chain(*res)
            return list(chain)
        except (KeyboardInterrupt, SystemExit):
            print "Caught exit, terminating"
            pool.terminate()
            exit()

    def get_command(self):
        return Command(self.settings['command'])

    def dump_all(self):
        command = self.get_command()
        repositories = self.get_repositories()
        command.backup_repos(repositories)
