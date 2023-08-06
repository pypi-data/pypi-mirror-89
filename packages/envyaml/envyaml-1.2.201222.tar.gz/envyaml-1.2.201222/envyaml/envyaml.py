# -*- coding: utf-8 -*-
# This file is part of EnvYaml project
# https://github.com/thesimj/envyaml
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import io
import os
import re

from yaml import safe_load

RE_COMMENTS = re.compile(r"(^#.*\n)", re.MULTILINE | re.UNICODE)
RE_DOT_ENV = re.compile(r"^((?!\d)[\w\- ]+=.*)$", re.MULTILINE | re.UNICODE)

RE_ENV = [
    (
        re.compile(r"(?<=\$\{)(.*?)(?=\})", re.MULTILINE | re.UNICODE),
        ["${{{match}}}"]
    ),
    (
        re.compile(r"(?<=[\"\']\$)(.*?)(?=[\"\']$)", re.MULTILINE | re.UNICODE),
        ['"${match}"', "'${match}'"],
    ),
    (
        re.compile(r"\$(?!\d)(.*)(?<![\s\]])", re.MULTILINE | re.UNICODE),
        ["{match}"]
    ),
]

__version__ = "1.2.201222"


class EnvYAML:
    __version__ = __version__

    DEFAULT_ENV_YAML_FILE = "env.yaml"  # type:str
    DEFAULT_ENV_FILE = ".env"  # type:str

    __env_file = None  # type:str
    __yaml_file = None  # type: str
    __cfg = None  # type: dict
    __strict = True  # type: bool

    def __init__(
        self, yaml_file=None, env_file=None, include_environment=True, strict=True
    ):
        """Create EnvYAML class instance and read content from environment and files if they exists

        :param str yaml_file: file path for config or env.yaml by default
        :param str env_file: file path for .env file or None by default
        :param bool include_environment: include environment variable, by default true
        :param bool strict: use strict mode and throw exception when have unset variable, by default true
        :return EnvYAML: new instance of EnvYAML
        """
        self.__strict = strict
        self.__env_file = env_file
        self.__yaml_file = yaml_file

        # read environment
        self.__cfg = dict(os.environ) if include_environment else {}

        # read .env file and update config
        self.__cfg.update(
            self.__read_env_file(
                self.__get_file_path(env_file, "ENV_FILE", self.DEFAULT_ENV_FILE),
                self.__strict,
            )
        )

        # read yaml file and update config
        self.__cfg.update(
            self.__read_yaml_file(
                self.__get_file_path(
                    yaml_file, "ENV_YAML_FILE", self.DEFAULT_ENV_YAML_FILE
                ),
                self.__cfg,
                self.__strict,
            )
        )

        # make config as flat dict with '.'
        self.__cfg = self.__flat(self.__cfg)

    def get(self, key, default=None):
        """Get configuration variable with default value. If no `default` value set use None

        :param any key: name for the configuration key
        :param any default: default value if no key found
        :return any:
        """

        return self.__cfg.get(key, default)

    def export(self):
        """Export config

        :return dict: dictionary with config
        """
        return self.__cfg.copy()

    @staticmethod
    def environ():
        """Get os.environ mapping object

        :return MutableMapping: A mapping object representing the string environment
        """
        return os.environ

    @staticmethod
    def __read_env_file(file_path, strict=True):
        """read and parse env file

        :param str file_path: path to file
        :param bool strict: strict mode
        :return dict:
        """
        config = {}

        if file_path:
            with io.open(file_path, encoding="utf8") as f:
                content = f.read()  # type: str

            # remove comments
            content = RE_COMMENTS.sub("", content)

            for line in RE_DOT_ENV.findall(content):
                name, value = line.strip().split("=", 1)  # type: str,str

                # strip names and values
                name = name.strip().strip("'\" ")
                value = value.strip().strip("'\" ")

                # set config
                config[name] = value

        return config

    @staticmethod
    def __read_yaml_file(file_path, cfg, strict, separator="|"):
        """read and parse yaml file

        :param str file_path: path to file
        :param dict cfg: configuration variables (environ and .env)
        :param bool strict: strict mode
        :return: dict
        """

        # read and parse files
        with io.open(file_path, encoding="utf8") as f:
            content = f.read()  # type:str

        # remove comments
        content = RE_COMMENTS.sub("", content)

        # fill variables and default values
        for re_env, templates in RE_ENV:
            for entry in re_env.finditer(content):
                match, group = entry.group(), entry.groups()[0]  # type: str, str

                # if group exist then get group
                kv = group if group else match[1:]  # type: str
                var_name, var_default = (
                    kv.split(separator) if separator in kv else (kv, None)
                )  # type: str, str

                if var_name in cfg:
                    for tm in templates:
                        # update match with template
                        content = content.replace(tm.format(match=match), cfg[var_name])

                elif var_name not in cfg and var_default is not None:
                    for tm in templates:
                        # update match with template
                        content = content.replace(tm.format(match=match), var_default)

                else:
                    if strict:
                        raise ValueError(
                            "Strict mode enabled, variable $"
                            + var_name
                            + " not defined!"
                        )

        # load content as yaml
        yaml = safe_load(content)

        # if contains somethings
        if yaml and isinstance(yaml, dict):
            return yaml

        # by default return empty dict
        return {}

    @staticmethod
    def __get_file_path(file_path, env_name, default):
        """Construct file path

        :param str file_path: path to file
        :param str env_name: env name
        :param str default: default file path
        :return str: return file path or None if file not exists
        """
        if file_path:
            return file_path

        elif os.environ.get(env_name):
            return os.environ.get(env_name)

        elif os.path.exists(default):
            return default

    @staticmethod
    def __flat_deep(prefix, config):
        """Flat siblings

        :param str prefix: prefix
        :param any config: configuration
        :return dict:
        """
        dest_ = {}

        elements = (
            enumerate(config)
            if (isinstance(config, list) or isinstance(config, tuple))
            else config.items()
        )  # type: (str, any)

        for key_, value_ in elements:
            key_ = prefix + "." + str(key_)

            if isinstance(value_, dict):
                dest_[key_] = value_
                dest_.update(EnvYAML.__flat_deep(key_, value_))

            elif isinstance(value_, list):
                dest_[key_] = value_
                dest_.update(EnvYAML.__flat_deep(key_, value_))

            else:
                dest_[key_] = value_

        return dest_

    @staticmethod
    def __flat(config):
        """Flat dictionaries in recursive way

        :param dict config: configuration
        :return dict:
        """
        dest_ = {}

        for key_, value_ in config.items():
            key_ = str(key_)

            if (
                isinstance(value_, dict)
                or isinstance(value_, list)
                or isinstance(value_, type)
            ):
                dest_[key_] = value_
                dest_.update(EnvYAML.__flat_deep(key_, value_))

            else:
                dest_[key_] = value_

        return dest_

    def format(self, key, **kwargs):
        """Apply quick format for string values with {arg}

        :param str key: key to argument
        :return str:
        """
        return self.__cfg[key].format(**kwargs)

    def keys(self):
        """Set-like object providing a view on keys"""
        return self.__cfg.keys()

    def __contains__(self, item):
        """Check if key in configuration

        :param any item: get
        :return: boo
        """
        return item in self.__cfg

    def __getitem__(self, key):
        """Get item ['item']

        :param str key: get environment name as item
        :return any:
        """

        return self.__cfg[key]


# export only this
__all__ = [__version__, EnvYAML]
