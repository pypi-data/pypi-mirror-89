import os
import yaml
from yaml import loader

try:
    from yaml import CLoader as YAMLLoader
except ImportError:
    from yaml import Loader as YAMLLoader

from dyncfg import middleware

os.environ.setdefault('DYN_YAML_CONF', 'config.yaml')


class Engine(middleware.Engine):

    @classmethod
    def config(cls, scope, key, cast=lambda x: x):
        conf = getattr(cls, '_cache_config', None)

        if not conf:
            try:
                with open(os.environ.get('DYN_YAML_CONF')) as fd:
                    conf = yaml.load(fd, Loader=YAMLLoader)
            except IOError:
                conf = {}

            cls._cache_config = conf

        default_conf = conf.get('default', {})
        scoped_conf = conf.get(scope, {})
        merged_conf = {**default_conf, **scoped_conf}

        return cast(merged_conf.get(key, None))
