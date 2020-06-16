"""
Configuration facility
"""

from typing import Any
import yaml

CONFIGURATION: dict


def load_configuration_file(path: str) -> None:
    """
    Loads the configuration from a YAML file.
    """
    global CONFIGURATION
    with open(path, 'r') as file:
        CONFIGURATION = yaml.safe_load(file.read())


def get(key: str, default: Any = None) -> Any:
    """
    Gets a config value from a key. Nested keys are separated by dots. For
    example::

        db_host = config.get('db.host', 'localhost')

    """
    keys = key.split('.')
    current: Any = CONFIGURATION
    for k in keys:
        if isinstance(current, dict):
            if k in current:
                current = current[k]
            else:
                return default
        else:
            return default
    return current
