#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-26 20:54:14
# Filename        : config.py
# Description     : 
from __future__ import unicode_literals

from ConfigParser import ConfigParser
from os import path

cfg_path = 'config.cfg'

class Section():
    def __init__(self, items):
        self._items = items

    def __getitem__(self, name):
        return self._items.get(name)

    def __getattr__(self, name):
        return self[name]

class Config():
    def __init__(self):
        assert path.isfile(cfg_path)
        self._cfg = ConfigParser()
        self._cfg.read(cfg_path)

    def __getitem__(self, name):
        return Section(dict(self._cfg.items(name)))

    def __getattr__(self, name):
        return self[name]

config = Config()
sync_config = config.sync

