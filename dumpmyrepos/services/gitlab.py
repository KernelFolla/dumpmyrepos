# -*- coding: utf-8 -*-

from __future__ import absolute_import
from dumpmyrepos.services.git import GitAccount, GitRepository
from gitlab import Gitlab


class GitlabRepository(GitRepository):
    def _get_ssh_url(self):
        return self.parent.ssh_url_to_repo


class GitlabAccount(GitAccount):
    _repo_class = GitlabRepository

    def _get_repositories_raw(self):
        gl = Gitlab(**self.config['auth'])
        gl.auth()
        return gl.projects.list()
