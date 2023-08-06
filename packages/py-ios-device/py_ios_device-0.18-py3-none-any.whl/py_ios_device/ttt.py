"""
@Date    : 2020-12-21
@Author  : liyachao
"""
import json
import sys
# print(11111)
# print(json.dumps(sys.path))
from py_ios_device import ios_device

def c(res):
    print(res)
# py_ios_device.get_network(c)
ios_device.get_channels(c)
