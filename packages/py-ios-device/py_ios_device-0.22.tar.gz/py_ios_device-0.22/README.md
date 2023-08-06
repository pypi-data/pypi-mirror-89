# py-ios-device 的 pip 仓库

Get IOS performance data through instruments protocol

win，mac 跨平台方案，通过 Instruments 私有协议获取 iOS 相关性能数据。

源码仓库地址: https://github.com/YueChen-C/py-ios-device

## 使用方法:
1.创建对象后获取数据:

```
from py_ios_device.py_ios_device import PyiOSDevice
device = PyiOSDevice("device_id")
device.connect()
pr = device.get_processes()
print(pr)
device.disconnect()
```
connect 后持续使用一个管道

2.单次使用
```
from py_ios_device import py_ios_device
pr = py_ios_device.get_processes("divece_id")
print(pr)
```

3.异步回调
```
from py_ios_device import py_ios_device

def c(res):
    print(res)

py_ios_device.get_network(c)
```


更新子仓库:

git pull origin main

git submodule foreach 'git pull origin main' 
