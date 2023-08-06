"""
@Date    : 2020-12-18
@Author  : liyachao
"""


class PyiOSDeviceException(Exception):
    def __init__(self, msg):
        self.msg = msg
