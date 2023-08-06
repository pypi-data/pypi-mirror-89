#!/usr/bin/python3

import time
import socket
import datetime
import platform

import psutil

print('-----------------------------CPU信息-------------------------------------')
# 查看cpu物理个数的信息
cpu_count = psutil.cpu_count(logical=False)
# CPU的使用率
cpu = (str(psutil.cpu_percent(1))) + '%'
print(u"物理CPU个数: %s  CUP使用率: %s" % (cpu_count, cpu))

print('-----------------------------内存信息-------------------------------------')
# 查看内存信息,剩余内存.free  总共.total
# round()函数方法为返回浮点数x的四舍五入值。
free = str(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 2))
total = str(round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2))
memory = int(psutil.virtual_memory().total - psutil.virtual_memory().free) / float(psutil.virtual_memory().total)
print(u"物理内存: %sG  剩余物理内存: %sG  物理内存使用率: %s%%" % (total, free, int(memory * 100)))

print('-----------------------------磁盘信息---------------------------------------')
disk = psutil.disk_usage("/")
total = int(disk.total / (1024.0 * 1024.0 * 1024.0))
free = int(disk.free / (1024.0 * 1024.0 * 1024.0))
print("总容量: %sG  可用容量: %sG" % (total, free))

print('-----------------------------网络信息---------------------------------------')
net = psutil.net_io_counters()
bytes_sent = '{0:.2f}Mb'.format(net.bytes_recv / 1024 / 1024)
bytes_rcvd = '{0:.2f}Mb'.format(net.bytes_sent / 1024 / 1024)
print(u"网卡接收流量: %s  网卡发送流量: %s" % (bytes_rcvd, bytes_sent))

print('-----------------------------系统信息-------------------------------------')
# 当前时间
now_time = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
print("当前时间: %s" % now_time)

# 系统启动时间
print(u"系统启动时间: %s" % datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))

# 系统用户
users_count = len(psutil.users())
users_list = ",".join([u.name for u in psutil.users()])
print(u"登录用户: %s个，分别是 %s" % (users_count, users_list))

sys_system = platform.system()  # 系统类型
sys_platform = platform.platform()  # 操作系统名称及版本号，'Windows-10-10.0.17134-SP0'
sys_version = platform.version()  # 操作系统版本号，'10.0.17134'
sys_architecture = platform.architecture()  # 操作系统的位数，('64bit', 'WindowsPE')
sys_machine = platform.machine()  # 硬件架构，'AMD64'
sys_node = platform.node()  # 网络名称，'TDM'
sys_processor = platform.processor()  # 处理器信息，'Intel64 Family 6 Model 158 Stepping 9, GenuineIntel'
sys_uname = platform.uname()  # 包含上面所有的信息汇总，

print("系统类型: %s" % sys_system)
print("系统版本: %s" % sys_version)
print("硬件架构: %s" % sys_machine)
print("处理器信息: %s" % sys_processor)
print("网络名称: %s" % sys_node)


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


if __name__ == '__main__':
    print("IP地址: %s" % get_host_ip())
