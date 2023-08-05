import os
import toml

from dyncfg import middleware

os.environ.setdefault('DYN_TOML_CONF', 'config.toml')

class Engine(middleware.Engine):

    @classmethod
    def config(cls, scope, key, cast=lambda x: x):
        conf = getattr(cls, '_cache_config', None)

        if not conf:
            try:
                with open(os.environ.get('DYN_TOML_CONF')) as fd:
                    conf = toml.load(fd)
            except IOError:
                conf = {}

            cls._cache_config = conf

        default_conf = conf.get('default', {})
        scoped_conf = conf.get(scope, {})
        merged_conf = {**default_conf, **scoped_conf}
        
        return cast(merged_conf.get(key, None))
