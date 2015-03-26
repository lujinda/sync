#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-26 21:19:40
# Filename        : handlers.py
# Description     : 
from __future__ import unicode_literals
from tornado.web import RequestHandler, HTTPError
from tornado.websocket import WebSocketHandler
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
    def token(self):
        _token = self.get_secure_cookie('token', None)
        if not _token:
            _token = made_token()
            self.set_secure_cookie('token', _token)

        return _token

    @property
    def server_manager(self):
        return self.application.server_manager

class SyncHandler(PublicHandler):
    def post(self):
        """数据格式：
            sync_data(用来生成数据库操作指令的): (json_str)db_name, collection_name, operation, args, kwargs,
            server_id(数据库id): (str)
        """
        print(self.request.arguments)

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

