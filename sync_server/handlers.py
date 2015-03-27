#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-27 19:20:32
# Filename        : handlers.py
# Description     : 
from __future__ import unicode_literals
from tornado.web import RequestHandler, HTTPError
from tornado.websocket import WebSocketHandler
from uuid import uuid4
import logging

from libs.wraps import only_one_inline
import json

class PublicHandler(RequestHandler):
    def initialize(self):
        self.init_data()

    def init_data(self):
        pass

    @property
    def db(self):
        return self.application.db

    @property
    def client_ip(self):
        return self.request.remote_ip

    @property
    def server_manager(self):
        return self.application.server_manager

    @property
    def allow_server_list(self):
        return self.application.allow_server_list

class SyncHandler(PublicHandler):
    def prepare(self):
        _server_id = self.get_argument('server_id', None)
        if (not _server_id) or (_server_id not in self.allow_server_list):
            raise HTTPError(403)
        self.from_server_id = _server_id

    def post(self):
        """数据格式：
            sync_data(用来生成数据库操作指令的): (json_str)db_name, collection_name, operation, args, kwargs,
            server_id(数据库id): (str)
        """
        sync_data = self.get_argument('sync_data')
        sync_id = str(uuid4().hex) # 每一个操作都对应着一个指令
        self.add_sync_data_queue(sync_id, sync_data)
        self.server_manager.broad_sync(server_id = self.from_server_id,
            response = {
                'sync_list' :{
                    sync_id     :   sync_data,
                    }
                }
            )

    def add_sync_data_queue(self, sync_id, sync_data):
        """把操作数据添加到除来源id的所有服务器对列中去"""
        for server_id in self.allow_server_list:
            if server_id == self.from_server_id:
                continue
            """添加sync_data到对应的server_id中去"""
            self.db.hset(server_id, sync_id, sync_data)

    def del_sync_data_queue(self, sync_ids):
        """删除某台服务器的某条sync记录，表示数据库服务器已将同步指令执行完成"""
        for sync_id in sync_ids.split(';'):
            self.db.hdel(self.from_server_id, sync_id)

    def delete(self):
        """数据格式:
            sync_id(同步数据的id)
            server_id (信息发送源的数据库服务器id)
            sync_id和server_id共同构成了一条特定的记录
        """
        sync_ids = self.get_argument('sync_ids') # 这里面可能有多条记录，以;隔开
        self.del_sync_data_queue(sync_ids)

    def get(self):
        response = {
                'server_id'     :   self.from_server_id,
                'sync_list'     :   self.db.hgetall(self.from_server_id),
                }
        self.write(response)

class ServerHandler(WebSocketHandler, PublicHandler):
    server_id = None
    def send_error_message(self, error):
        self.write_response({'error': error})
        self.close()

    def open(self):
        logging.info('有来自 %s 数据库服务器连接' % (self.client_ip))
    
    def on_message(self, server_id):
        self.register_server(server_id) # 注册服务器

    def on_close(self):
        """断开连接时，就注册服务器"""
        self.unregister_server()

    @only_one_inline
    def register_server(self, server_id):
        self.server_id = server_id
        self.server_manager.register(self)

        logging.info('%s 数据库连接成功' % self.server_id)

    def unregister_server(self):
        self.server_manager.unregister(self)
        logging.info('%s 数据库已断开连接' % self.server_id)

    def on_close(self):
        self.unregister_server()

    def write_response(self, response):
        if isinstance(response, dict):
            response = json.dumps(response)

        self.write_message(response)

