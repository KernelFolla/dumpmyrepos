# -*- coding: utf-8 -*-

from .git import GitAccount
from .bitbucket import BitbucketAccount
from .github import GithubAccount
from .gitlab import GitlabAccount


def factory(name, config):
    # type: (str, object) -> GitAccount
    class_ = classes[config['type']]
    return class_(name, config)


classes = {
    'git': GitAccount,
    'gitlab': GitlabAccount,
    'bitbucket': BitbucketAccount,
    'github': GithubAccount,
}
