#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-26 20:09:07
# Filename        : run.py
# Description     : 
from __future__ import unicode_literals
import websocket
from app import SyncWebSocketApp
from time import sleep

if __name__ == '__main__':
#    websocket.enableTrace(True)
    while True:
        ws_app = SyncWebSocketApp()
        ws_app.run_forever(ping_interval = 10) 
        if ws_app.abort_exit:
            break
        sleep(1)

