#!/usr/bin/env python
#coding:utf8 # Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-27 19:23:05
# Filename        : sync.py
# Description     : 
from __future__ import unicode_literals
from config import sync_config
from pymongo import Connection
import json
from requests import delete, get

db_connection = Connection()

def fetch_sync_list(server_id):
    assert server_id == sync_config.server_id
    _get_data = {
            'server_id'     :       server_id,
            }
    response = get(sync_config.sync_url, data = _get_data).json()
    sync_handler = SyncHandler(response)
    if sync_handler.exec_sync():
        sync_handler.reply_sync()

class SyncHandler():
    def __init__(self, response):
        self.server_id = response['server_id']
        assert self.server_id == sync_config.server_id

        self.sync_list = response['sync_list']
        self.finished_list = []

    def exec_sync(self):
        for sync_id, sync_data in self.sync_list.items():
            sync_data = json.loads(sync_data)
            if self.__exec_sync(sync_data): # 如果执行成功，则把当前的sync_id加到一个列表中去
                self.finished_list.append(sync_id)

        return bool(len(self.finished_list))

    def __exec_sync(self, sync_data):
        """把指令组装起来，然后执行它"""
        _db = db_connection[sync_data['db_name']]
        _collection = getattr(_db, sync_data['collection_name'])
        _func = getattr(_collection, sync_data['operation'])
        try:
            _func(*sync_data['args'], **sync_data['kwargs'])
        except:
            return False
        return True

    def reply_sync(self):
        assert self.finished_list
        _delete_data = {
                'server_id'     :   self.server_id,
                'sync_ids'       :   ';'.join(self.finished_list),
                }
        delete(sync_config.sync_url, data = _delete_data)

