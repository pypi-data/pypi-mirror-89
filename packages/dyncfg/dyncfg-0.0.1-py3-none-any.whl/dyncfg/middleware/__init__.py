
from typing import AbstractSet


class Engine(object):

    @classmethod
    def config(cls, scope, key, cast=lambda x: x):
        raise NotImplementedError()
