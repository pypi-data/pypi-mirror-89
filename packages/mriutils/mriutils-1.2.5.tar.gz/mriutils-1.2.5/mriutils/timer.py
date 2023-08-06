#!/usr/bin/env python

import time

class Timer():
    def __init__(self):
        pass
    
    def localTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    def timeZone(self):
        return time.timezone()
    
