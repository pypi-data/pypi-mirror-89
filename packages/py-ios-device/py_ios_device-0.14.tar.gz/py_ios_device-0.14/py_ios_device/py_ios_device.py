"""
@Date    : 2020-12-18
@Author  : liyachao
"""
import json
from _ctypes import Structure
from ctypes import c_byte, c_uint16, c_uint32

from demo.instrument_services.activity import activity as _activity
from demo.instrument_services.channel import channels as _channels
from demo.instrument_services.launch_app import launch_app as _launch_app
from demo.instrument_services.networking import networking as _networking
from demo.instrument_services.runningProcesses import runningProcesses as _runningProcesses
from demo.instrument_services.sysmontap import sysmontap as _sysmontap
from instrument.RPC import get_usb_rpc, InstrumentRPC
from instrument.dtxlib import auxiliary_to_pyobject
from py_ios_device.util.exeption import PyiOSDeviceException
from py_ios_device.util.utils import caller
from socket import inet_ntoa, htons, inet_ntop, AF_INET6


class PyiOSDevice:
    def __init__(self, device_id: str = None):
        self._device_id = device_id
        self._rpc = None

    def connect(self):
        self._rpc = get_usb_rpc(self._device_id)

    def disconnect(self):
        self._rpc.deinit()

    def get_network(self, on_callback):
        get_network(on_callback, self._device_id, self._rpc)

    def get_processes(self):
        return get_processes(self._device_id, self._rpc)

    def get_performance_by_process(self, pid: int, on_callback):
        get_performance_by_process(pid, on_callback, self._device_id, self._rpc)

    def get_performance_by_bundle_id(self, bundle_id: str, on_callback):
        get_performance_by_bundle_id(bundle_id, on_callback, self._device_id, self._rpc)

    def launch_app_callback(self, bundle_id, on_callback):
        launch_app_callback(bundle_id, on_callback, self._device_id, self._rpc)

    def launch_app(self, bundle_id):
        launch_app(bundle_id, self._device_id, self._rpc)

    def get_all_process_performance(self, on_callback):
        get_all_process_performance(on_callback, self._device_id, self._rpc)

    def get_channels(self, on_callback):
        get_channels(on_callback, self._device_id, self._rpc)


def get_network(on_callback=None, device_id: str = None, rpc: InstrumentRPC = None):
    """
    获取设备的网络信息
    :param device_id: 设备id
    :param on_callback: 回调函数
    :param rpc: 设备连接
    :return:
    """

    headers = {
        0: ['InterfaceIndex', "Name"],
        1: ['LocalAddress', 'RemoteAddress', 'InterfaceIndex', 'Pid', 'RecvBufferSize', 'RecvBufferUsed',
            'SerialNumber', 'Kind'],
        2: ['RxPackets', 'RxBytes', 'TxPackets', 'TxBytes', 'RxDups', 'RxOOO', 'TxRetx', 'MinRTT', 'AvgRTT',
            'ConnectionSerial']
    }

    class SockAddr4(Structure):
        _fields_ = [
            ('len', c_byte),
            ('family', c_byte),
            ('port', c_uint16),
            ('addr', c_byte * 4),
            ('zero', c_byte * 8)
        ]

        def __str__(self):
            return f"{inet_ntoa(self.addr)}:{htons(self.port)}"

    class SockAddr6(Structure):
        _fields_ = [
            ('len', c_byte),
            ('family', c_byte),
            ('port', c_uint16),
            ('flowinfo', c_uint32),
            ('addr', c_byte * 16),
            ('scopeid', c_uint32)
        ]

        def __str__(self):
            return f"[{inet_ntop(AF_INET6, self.addr)}]:{htons(self.port)}"

    def net_callback(res):
        data = res.parsed
        if data[0] == 1:
            if len(data[1][0]) == 16:
                data[1][0] = str(SockAddr4.from_buffer_copy(data[1][0]))
                data[1][1] = str(SockAddr4.from_buffer_copy(data[1][1]))
            elif len(data[1][0]) == 28:
                data[1][0] = str(SockAddr6.from_buffer_copy(data[1][0]))
                data[1][1] = str(SockAddr6.from_buffer_copy(data[1][1]))
        caller(dict(zip(headers[data[0]], data[1])), on_callback)

    _rpc = rpc

    if not rpc:
        _rpc = get_usb_rpc(device_id)
    if not on_callback:
        raise PyiOSDeviceException("on_callback can not be null")

    _networking(_rpc, net_callback)

    if not rpc:
        _rpc.stop()


def get_processes(device_id: str = None, rpc: InstrumentRPC = None):
    """
    获取设备中的进程列表
    :param device_id:
    :param rpc: 设备连接
    :return:
    """
    _rpc = rpc
    if not rpc:
        _rpc = get_usb_rpc(device_id)

    processes_list = _runningProcesses(_rpc)
    if not rpc:
        _rpc.stop()
    return processes_list


def get_performance_by_process(pid: int, on_callback, device_id: str = None, rpc: InstrumentRPC = None):
    """
    使用进程 id 获取性能数据
    :param pid:
    :param on_callback:
    :param device_id:
    :param rpc: 设备连接
    :return:
    """
    _rpc = rpc
    if not rpc:
        _rpc = get_usb_rpc(device_id)
    if not pid:
        raise PyiOSDeviceException("pid can not be null")

    def _on_callback(res):
        caller(res, on_callback)

    _activity(_rpc, pid, _on_callback)

    if not rpc:
        _rpc.stop()


def get_performance_by_bundle_id(bundle_id: str, on_callback, device_id: str = None, rpc: InstrumentRPC = None):
    """
    使用包名获取性能数据
    :param bundle_id:
    :param on_callback:
    :param device_id:
    :param rpc: 设备连接
    :return:
    """
    if not bundle_id:
        raise PyiOSDeviceException("bundle_id can not be null")
    process_list = get_processes(device_id)
    for _index in process_list:
        if _index.get("name") == bundle_id:
            return get_performance_by_process(_index.get("pid"), on_callback, device_id, rpc)
    raise Exception("No application with bundle ID [{}] was found".format(bundle_id))


def launch_app_callback(bundle_id: str, on_callback, device_id: str = None, rpc: InstrumentRPC = None):
    """
    启动应用
    :param bundle_id:
    :param device_id:
    :param on_callback:
    :param rpc: 设备连接
    :return:
    """
    if not bundle_id:
        raise PyiOSDeviceException("bundle_id can not be null")
    _rpc = rpc
    if not on_callback:
        raise PyiOSDeviceException("on_callback can not be null")
    if not rpc:
        _rpc = get_usb_rpc(device_id)

    def _callback(res):
        if res.raw._auxiliaries:
            for buf in res.raw._auxiliaries:
                caller(auxiliary_to_pyobject(buf), on_callback)

    _launch_app(_rpc, bundle_id, _callback)
    if not rpc:
        _rpc.stop()


def launch_app(bundle_id: str, device_id: str = None, rpc: InstrumentRPC = None):
    if not bundle_id:
        raise PyiOSDeviceException("bundle_id can not be null")
    _rpc = rpc

    if not rpc:
        _rpc = get_usb_rpc(device_id)

    def _callback(res):
        pass

    _launch_app(_rpc, bundle_id, _callback)
    if not rpc:
        _rpc.stop()


def get_all_process_performance(on_callback, device_id: str = None, rpc: InstrumentRPC = None):
    """
    获取所有进程的性能数据
    :param on_callback:
    :param device_id:
    :param rpc:
    :return:
    """
    _rpc = rpc
    if not on_callback:
        raise PyiOSDeviceException("on_callback can not be null")
    if not rpc:
        _rpc = get_usb_rpc(device_id)

    def _callback(res):
        if isinstance(res.parsed, list):
            caller(json.dumps(res.parsed, indent=4), on_callback)

    _sysmontap(_rpc, _callback)
    if not rpc:
        _rpc.stop()


def get_channels(on_callback, device_id: str = None, rpc: InstrumentRPC = None):
    """
    获取可用服务列表
    :param on_callback:
    :param device_id:
    :param rpc:
    :return:
    """
    if not on_callback:
        raise PyiOSDeviceException("on_callback can not be null")
    _rpc = rpc
    if not rpc:
        _rpc = get_usb_rpc(device_id)

    def _on_callback(res):
        _dict = dict()
        for k, v in auxiliary_to_pyobject(res.raw._auxiliaries[0]).items():
            _dict[k] = v
        caller(_dict, on_callback)

    _channels(_rpc, _on_callback)
    if not rpc:
        _rpc.stop()
