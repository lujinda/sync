#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-27 17:31:45
# Filename        : app.py
# Description     : 
from tornado.web import Application
from handlers import ServerHandler, SyncHandler
from libs.sync import ServerManager
from redis import Redis

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
        self.allow_server_list = ('jifang', 'vps')
        self.db = Redis(db = 4) # 存放着每台数据库服务器需要同步的指令队列

        super(DemoApplication, self).__init__(handlers, **settings)

