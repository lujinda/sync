#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-26 21:15:28
# Filename        : app.py
# Description     : 
from tornado.web import Application
from handlers import ServerHandler, SyncHandler
from libs.sync import ServerManager

class DemoApplication(Application):
    def __init__(self):
        handlers = [
                (r'/server', ServerHandler), # websocket的链接 
                (r'/sync', SyncHandler), # 用于同步的
                ]
        settings = {
                'debug': True,
                'cookie_secret': 'aaaaaaa',
                }

        self.server_manager = ServerManager()   # 管理数据库服务器连接的

        super(DemoApplication, self).__init__(handlers, **settings)

