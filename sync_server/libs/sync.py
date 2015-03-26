#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-26 21:16:06
# Filename        : libs/sync.py
# Description     : 

class ServerManager():
    server_list = {}

    def register(self, server):
        self.server_list[server.server_id] = server

    def unregister(self, server):
        self.server_list.pop(server.server_id, None)

    def server_is_inline(self, server_id):
        return server_id in self.server_list

