#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-27 20:02:14
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

    def broad_sync(self, from_server_id, response):
        for server_id in self.server_list:
            if server_id == from_server_id: # 如果广播对象是自己的话，就不广播了
                continue
            response['server_id'] =  server_id
            server = self.server_list[server_id]
            server.write_response(response)

