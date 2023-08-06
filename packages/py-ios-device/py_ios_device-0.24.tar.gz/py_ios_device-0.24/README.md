# py-ios-device 的 pip 仓库

Get IOS performance data through instruments protocol

win，mac 跨平台方案，通过 Instruments 私有协议获取 iOS 相关性能数据。

源码仓库地址: https://github.com/YueChen-C/py-ios-device

### 安装:

pip3 install py_ios_device

### 使用方法:
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
from py_ios_device import ios_device
pr = ios_device.get_processes("divece_id")
print(pr)
```

3.异步回调
```
from py_ios_device import ios_device

def c(res):
    print(res)

ios_device.get_network(c)
```

### api

get_network  # 获取网络信息

get_processes  # 获取进程列表

get_performance_by_process  # 根据设备中的进程 id 获取性能数据

get_performance_by_bundle_id  # 根据包名获取性能数据

launch_app  # 启动 app

launch_app_callback   # 启动 app 具有回调函数

get_all_process_performance  # 获取所有进程的性能数据




更新子仓库:

git pull origin main

git submodule foreach 'git pull origin main' 
