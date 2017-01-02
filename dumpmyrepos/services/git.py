# -*- coding: utf-8 -*-

import re


class GitRepository:
    _REPO_RE = re.compile(r'([a-zA-Z0-9._-]+)/([a-zA-Z0-9._-]+).git$')

    def __init__(self, parent, account):
        # type: (any, GitAccount) -> GitRepository
        self.parent = parent
        self.account = account
        self.ssh_url = self._get_ssh_url()
        self.team_name = self._get_team_name()
        self.project_name = self._get_project_name()

    def __str__(self):
        return self.ssh_url

    def _get_ssh_url(self):
        return self.parent

    def _get_team_name(self):
        m = self._REPO_RE.search(self.ssh_url)
        return m.group(1) if m else 'error'

    def _get_project_name(self):
        m = self._REPO_RE.search(self.ssh_url)
        return m.group(2) if m else 'error'


class GitAccount:
    _repo_class = GitRepository

    def __init__(self, name, config):
        self.name = name
        self.config = config

    def __str__(self):
        return self.name

    def get_repositories(self):
        # type: (str, object) -> list[GitRepository]
        class_ = self._repo_class
        return map(lambda x: class_(x, self), self._get_repositories_raw())

    def _get_repositories_raw(self):
        return self.config['repositories']
