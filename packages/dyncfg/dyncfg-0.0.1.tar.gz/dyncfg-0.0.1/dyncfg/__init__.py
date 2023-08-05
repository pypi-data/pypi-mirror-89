import os
import re

from logging import getLogger
from importlib import import_module

os.environ.setdefault('DYNCFG_ENV', 'development')

__version__ = '0.0.1'

DYNCFG_MIDDLEWARE = (
    'dyncfg.middleware.toml',
    'dyncfg.middleware.yaml',
    'dyncfg.middleware.json',
)

log = getLogger('dyncfg')

class ValidationKeyError(Exception):

    def __init__(self, key):
        super().__init__(f'Key "{key}" is not valid')

def _is_key_valid(key):
    validator = re.compile('^([a-z]|[A-Z]|_)([a-z]|[A-Z]|_|[0-9])*$')

    if not validator.match(key):
        raise ValidationKeyError(key)
        

def config(key, default=None, cast=lambda x: x):
    scope = os.environ.get('DYNCFG_ENV')
    value = None

    _is_key_valid(key)

    for engine in DYNCFG_MIDDLEWARE:
        log.info(f'Usign engine "{engine}"')
        value = import_module(engine).Engine.config(scope, key, cast)

        if value:
            log.info(f'Value found in engine "{engine}"')
            break
        else:
            log.info(f'Value not found in engine "{engine}"')

    return os.path.expandvars(cast(value if value else default))