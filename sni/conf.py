"""
Configuration facility
"""

import collections
from typing import Any, List, MutableMapping, Tuple
import logging
import yaml

CONFIGURATION: dict


def assert_set(key: str) -> None:
    """
    Raises an exception if the configuration dict does not have that key.
    """
    if key not in CONFIGURATION:
        raise RuntimeError(f'Configuration key {key} not set')


def load_configuration_file(path: str) -> None:
    """
    Loads the configuration from a YAML file.

    Also sets default values.
    """
    with open(path, 'r') as file:
        file_config = yaml.safe_load(file.read())
    global CONFIGURATION
    CONFIGURATION = flatten_dict(file_config)
    CONFIGURATION['logging'] = file_config.get('logging', {})
    set_default('db.database', 'sni')
    set_default('db.driver', 'default')
    assert_set('db.host')
    assert_set('db.password')
    set_default('db.port', 3306)
    set_default('db.type', 'mysql')
    set_default('db.username', 'sni')
    assert_set('esi.client_id')
    assert_set('esi.client_secret')
    set_default('general.debug', False)
    set_default('general.host', '127.0.0.1')
    set_default('general.port', '5000')
    assert_set('general.root_url')
    set_default('jwt.algorithm', 'HS256')
    assert_set('jwt.secret')
    set_default('redis.database', 'sni')
    assert_set('redis.host')
    set_default('redis.port', 6379)


def flatten_dict(nested_dict: MutableMapping[Any, Any],
                 parent_key: str = '',
                 separator: str = '.') -> dict:
    """
    Flattens a dictionnary.

    `Credits to Imran <https://stackoverflow.com/a/6027615>`_.

    >>> flatten_dict({
        'a': 1, 'c': {'a': 2, 'b': {'x': 5, 'y' : 10}},
        'd': [1, 2, 3],
    })
    {'a': 1, 'c_a': 2, 'c_b_x': 5, 'd': [1, 2, 3], 'c_b_y': 10}

    """
    items: List[Tuple[Any, Any]] = []
    for key, val in nested_dict.items():
        new_key = parent_key + separator + key if parent_key else key
        if isinstance(val, collections.MutableMapping):
            items.extend(flatten_dict(val, new_key, separator).items())
        else:
            items.append((new_key, val))
    return dict(items)


def get(key: str, default: Any = None) -> Any:
    """
    Gets a config value from a key.
    """
    if key in CONFIGURATION:
        return CONFIGURATION[key]
    logging.warning('Unknown configuration key %s', key)
    return default


def set_default(key: str, val: Any) -> None:
    """
    Sets a configuration value if none is present at the key.
    """
    global CONFIGURATION
    if key not in CONFIGURATION:
        CONFIGURATION[key] = val
