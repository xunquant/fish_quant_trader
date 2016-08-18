# -*- coding: utf-8 -*-
import os,socket,fcntl,struct

def isInuseWindow(port):
    if os.popen('netstat -an | findstr :' + str(port)).readlines():
        portIsUse = True
    else:
        portIsUse = False
    return portIsUse

def isInuseLinux(port):
	#lsof -i:4906
	#not show pid to avoid complex
	if os.popen('netstat -na | grep :' + str(port)).readlines():
		portIsUse = True
	else:
		portIsUse = False
	return portIsUse

def scan_available_ports_then_return(platform_category):
	'''
	从65535开始向下扫描一个能用的端口，并返回
	'''

	if 'windows' in platform_category:
		port_judging=isInuseWindow
	else:
		port_judging=isInuseLinux

	for each_port in range(65535,0,-1):
		if not port_judging(each_port):
			return each_port
		else:
			continue
		pass
	pass

def get_ip_of_a_net_adapter_in_linux(device_name):
	s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, # SIOCGIFADDR
		struct.pack('256s', device_name[:15]))[20:24])

def get_local_ip(platform_category):
	'''
	取得本机IP地址
	'''

	if platform_category.__contains__('windows'):#如果是windows，未完成
		host_name=socket.gethostname()
		my_host_name=socket.getfqdn()
		#获取本机ip
		ip_list=socket.gethostbyname_ex(my_host_name)
		my_local_ip=socket.gethostbyname(my_host_name)
	else:#linux系统
		try:
			my_local_ip=get_ip_of_a_net_adapter_in_linux('eth0')#此处指定硬网卡的设备名称,如果叫做eth0
		except:
			try:
				my_local_ip=get_ip_of_a_net_adapter_in_linux('p4p1')#此处指定硬网卡的设备名称,如果叫做p4p1
			except:
				my_local_ip='请注意检查网卡在本机的名称，并在源代码中添加'
				print my_local_ip
		pass
	return my_local_ip
	pass