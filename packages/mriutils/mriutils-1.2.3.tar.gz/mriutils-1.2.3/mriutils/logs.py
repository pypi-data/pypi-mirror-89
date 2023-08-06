#!/usr/bin/env python

class Logs():
    def __init__(self):
        pass

    def printLogs(self, level = 0, filename = None, content = None):
        if level == 0:
            print('DEBUG [%s] %s' %(filename, content))
        elif level == 1:
            print('RELEASE [%s] %s' %(filename, content))