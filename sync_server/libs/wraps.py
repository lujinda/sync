#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-26 19:15:30
# Filename        : libs/wraps.py
# Description     : 
from __future__ import unicode_literals

from functools import wraps

def only_one_inline(func):
    def wrap(self, server_id):
        if self.server_manager.server_is_inline(server_id):
            self.send_error_message('{server_id} 已在线，请不要多次连接'.format(server_id = server_id))
        else:
            return func(self, server_id)

    return wrap

