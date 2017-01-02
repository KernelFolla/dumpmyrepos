# -*- coding: utf-8 -*-

from .git import GitAccount, GitRepository
from pybitbucket.auth import OAuth1Authenticator, BasicAuthenticator
from pybitbucket.bitbucket import Client
from pybitbucket.repository import Repository, RepositoryRole


class BitbucketRepository(GitRepository):
    def _get_ssh_url(self):
        return self.parent.clone['ssh'] \
            .replace('ssh://', '') \
            .replace('bitbucket.org/', 'bitbucket.org:')


class BitbucketAccount(GitAccount):
    _repo_class = BitbucketRepository

    def _get_repositories_raw(self):
        if 'username' in self.config['auth']:
            bb = Client(BasicAuthenticator(**self.config['auth']))
        else:
            bb = Client(OAuth1Authenticator(**self.config['auth']))

        return Repository.find_repositories_by_owner_and_role(
            role=RepositoryRole.MEMBER.value,
            client=bb
        )
