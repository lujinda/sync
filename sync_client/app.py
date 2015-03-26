#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-26 21:36:15
# Filename        : app.py
# Description     : 
from __future__ import unicode_literals

from websocket import WebSocketApp
from config import sync_config
import sys
import json


class SyncWebSocketApp(WebSocketApp):
    abort_exit = False
    def __init__(self):
        super(SyncWebSocketApp, self).__init__(sync_config.ws_url,
                on_open = self.on_open,
                on_message = self.on_message,
                on_error = self.on_error,
                on_close = self.on_close)

    def on_open(self, ws):
        ws.send(sync_config.server_id) # 建立连接后，向服务器发送自己的id，以完成注册

    def on_message(self, ws, message):
        response = json.loads(message)
        error = response.get('error', None) # 如果命令中带有error，则表示是出错信息，则需要输出，并停止任务
        if error:
            self.print_error(error)
            return

        print(response)

    def print_error(self, error):
        sys.stderr.write(error + '\n')
        self.abort_exit = True

    def print_info(self, info):
        sys.stdout.write(info + '\n')

    def on_error(self, ws, error):
        self.print_error(error)

    def on_close(self, ws):
        self.print_info('close')

