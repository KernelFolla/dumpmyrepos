# -*- coding: utf-8 -*-

from .git import GitAccount
from .bitbucket import BitbucketAccount
from .github import GithubAccount
from .gitlab import GitlabAccount

CLASSES = {
    'git': GitAccount,
    'gitlab': GitlabAccount,
    'bitbucket': BitbucketAccount,
    'github': GithubAccount
}


def factory(name, config):
    # type: (str, object) -> GitAccount
    return CLASSES[config['type']](name, config)
