# -*- coding: utf-8 -*-

from .services.git import GitRepository
from random import shuffle
from multiprocess import Pool
import datetime
import os
import subprocess
import sys
import traceback
import logging


class Command:
    def __init__(self, settings):
        self._verbose = settings.get('verbose', False)
        self._quiet = settings.get('quiet', False)
        self._dry_run = settings.get('dry_run', False)
        self._max_attempts = settings.get('max_attempts', 4)
        self._cmd_clone = settings.get('cmd_clone', 'git clone --mirror')
        self._cmd_update = settings.get('cmd_update', 'git remote update --prune')
        self._base_path = os.path.abspath(settings.get('base_path', '.'))
        self._parallel_downloads = settings.get('parallel_downloads', 1)

    def debug(self, message, output_no_verbose=False):
        """
        Outputs a message to stdout taking into account the options verbose/quiet.
        """
        if not self._quiet and (output_no_verbose or self._verbose):
            print("%s - %s" % (datetime.datetime.now(), message))

    def exit(self, message, code=1):
        """
        Forces script termination using C based error codes.
        By default, it uses error 1 (EPERM - Operation not permitted)
        """
        if not self._quiet and message and len(message) > 0:
            sys.stderr.write("%s (%s)\n" % (message, code))
        sys.exit(code)

    def exec_cmd(self, command):
        """
        Executes an external command taking into account errors and logging.
        """
        self.debug("Executing command: %s" % command)
        if self._dry_run:
            print(command)
            return
        if not self._verbose:
            if 'nt' == os.name:
                command = "%s > nul 2> nul" % command
            else:
                command = "%s > /dev/null 2>&1" % command

        resp = subprocess.call(command, shell=True)
        if resp != 0:
            self.exit("Command [%s] failed" % command, resp)

    def backup_repo(self, repo):
        # type: (GitRepository) -> Null
        self.debug("Backing up [%s]..." % repo, True)
        backup_dir = self._base_path + '/' + os.path.join(repo.account.name, repo.team_name, repo.project_name)
        for attempt in range(1, self._max_attempts + 1):
            try:
                if not os.path.isdir(backup_dir):
                    self.clone_repo(repo, backup_dir)
                else:
                    self.update_repo(repo, backup_dir)
            except SystemExit:
                self.debug("Failed to backup repository [%s], keep trying, %d attempts remain" % (
                    repo, self._max_attempts - attempt))
            else:
                break

    # todo: find a way to break everything on keyboard interrupt
    def _parallelize(self, call, items):
        pool = Pool(self._parallel_downloads)
        self.__terminated = False
        try:
            shuffle(items)
            pool.map_async(lambda x: call(x), items).get(9999999)
            pool.close()
            pool.join()
        except (KeyboardInterrupt, SystemExit):
            self.debug("Caught exit, terminating")
            pool.terminate()

    def backup_repos(self, repositories):
        if self._parallel_downloads > 1:
            self._parallelize(lambda repo: self.backup_repo(repo), repositories)
        else:
            for x in repositories:
                self.backup_repo(x)

    def clone_repo(self, repo, backup_dir):
        # type: (GitRepository, string) -> Null
        command = (self._cmd_clone + " %s %s") % (repo.ssh_url, backup_dir)
        self.exec_cmd(command)
        self.debug("Cloned [%s] into [%s]..." %  (repo, backup_dir), True)

    def update_repo(self, repo, backup_dir):
        os.chdir(backup_dir)
        command = self._cmd_update
        self.exec_cmd(command)
        self.debug("Updated [%s] into [%s]..." % (repo, backup_dir), True)
