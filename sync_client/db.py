#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-27 16:42:52
# Filename        : db.py
# Description     : 

from requests import post
import json

from config import sync_config

class DB():
    """封装了mongodb数据库的接口"""
    def __init__(self, db):
        self._db = db

    def __getitem__(self, name):
        return Collection(getattr(self._db, name)) 

    def __getattr__(self, name):
        return self[name]

class Collection():
    """重新封装mongodb的collection"""
    def __init__(self, collection):
        self._collection = collection
    
    def __getitem__(self, name):
        return self._collection[name]

    def __getattr__(self, name):
        return getattr(self._collection, name)

    def update_sync(self, *args, **kwargs):
        return self.__sync('update', *args, **kwargs)

    def insert_sync(self, *args, **kwargs):
        return self.__sync('insert', *args, **kwargs)

    def remove_sync(self, *args, **kwargs):
        return self.__sync('remove', *args, **kwargs)

    def __sync(self, operation,  *args, **kwargs):
        db_name, collection_name = self.full_name.split('.', 1)
        _sync_data = { # 组成数据同步指令的参数
                'db_name'           :   db_name,
                'collection_name'   :   collection_name,
                'operation'         :   operation,
                'args'              :   args,
                'kwargs'            :   kwargs,
                }

        _post_data = {
                'sync_data'     :   json.dumps(_sync_data),
                'server_id'     :   sync_config.server_id,
                }

        post(sync_config.sync_url, _post_data)

        return getattr(self, operation)(*args, **kwargs)

