#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2015-03-26 18:10:06
# Filename        : run.py
# Description     : 
from tornado import options, ioloop, httpserver
from tornado.options import options, define
from app import DemoApplication

define('port', type=int, default=1234, help='listen given port')

if __name__ == "__main__":
    options.parse_command_line()
    http_server = httpserver.HTTPServer(DemoApplication())
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()

