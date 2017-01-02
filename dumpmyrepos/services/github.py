# -*- coding: utf-8 -*-

from dumpmyrepos.services.git import GitAccount, GitRepository
from pygithub3 import Github


class GithubRepository(GitRepository):
    def _get_ssh_url(self):
        return self.parent.ssh_url


class GithubAccount(GitAccount):
    _repo_class = GithubRepository

    def _get_repositories_raw(self):
        gh = Github(**self.config['auth'])
        return gh.repos.list().all()
