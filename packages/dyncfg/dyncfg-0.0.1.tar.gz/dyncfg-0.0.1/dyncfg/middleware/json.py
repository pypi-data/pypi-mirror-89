import os
import json

from dyncfg import middleware

os.environ.setdefault('DYN_JSON_CONF', 'config.json')

class Engine(middleware.Engine):

    @classmethod
    def config(cls, scope, key, cast=lambda x: x):
        conf = getattr(cls, '_cache_config', None)

        if not conf:
            try:
                with open(os.environ.get('DYN_JSON_CONF')) as fd:
                    conf = json.load(fd)
            except IOError:
                conf = {}

            cls._cache_config = conf

        default_conf = conf.get('default', {})
        scoped_conf = conf.get(scope, {})
        merged_conf = {**default_conf, **scoped_conf}
        
        return cast(merged_conf.get(key, None))
