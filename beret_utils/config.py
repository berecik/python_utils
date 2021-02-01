import os
from abc import abstractmethod

from .mapping import MappingConst
from .singleton import Singleton


class Value(object):

    def __call__(self, env):
        return self.get_value(env)

    @abstractmethod
    def get_value(self, config):
        pass


class EnvValue(Value):
    def __init__(self, var_name):
        self.var_name = var_name

    def get_value(self, env):
        return env[self.var_name]


@Singleton
class ConfigBaseClass(MappingConst):

    DEFAULTS = []
    ENV_FILES = []

    def get_env(self):
        env = {}  # dict(os.environ)
        self.__dict__ = {}
        for env_file_path in self.ENV_FILES:
            try:
                with open(env_file_path, 'r') as env_file:
                    for line in env_file.readlines():
                        line = line.strip()
                        if '=' in line and line[0] != '#':
                            try:
                                key, value = line.split('=')
                                env[key] = value
                            except ValueError:
                                pass
            except FileNotFoundError:
                pass
        env.update(os.environ)
        return env

    def get_values(self):
        values = {}
        env = self.get_env()
        for key, value, parser, env_key in self.DEFAULTS:
            if env_key in env:
                value = parser(env[env_key])
            if callable(value):
                value = value(env)
            values[key] = value
        return values

    def __init__(self):
        self.__dict__ = self.get_values()
        super().__init__()


def get_config(defaults, env_files):

    class ConfigClass(ConfigBaseClass):
        DEFAULTS = tuple(
            map(
                lambda args:
                (lambda key, value=None, parser=str, env_key=None:
                 (
                     key,
                     value,
                     parser,
                     key if env_key is None else env_key
                 )
                 )(*args),
                defaults
            )
        )
        ENV_FILES = env_files

    return ConfigClass