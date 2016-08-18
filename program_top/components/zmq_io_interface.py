# -*- coding: utf-8 -*-

from zmq.eventloop.zmqstream import ZMQStream
from zmq import Context,PULL,PUSH
from program_top.utilities.ip_and_socket import get_local_ip
from program_top.components import component_base

class zmq_listen_connection(object):
	'''zmq监听连接'''
	def __init__(self,port_number,callback_function):
		'''
		端口号
		指定处理消息回调函数，消息作为入参
		'''
		super(zmq_listen_connection, self).__init__()
		self.__context=Context()
		self.__socket=self.__context.socket(PULL)
		self.__socket.bind("tcp://0.0.0.0:%d"%(port_number))
		self.__stream_pull=ZMQStream(self.__socket)
		self.__stream_pull.on_recv(callback_function)
		pass
	pass

class zmq_send_connection(object):
	'''zmq发送连接'''
	def __init__(self):
		self.__context=Context()
		self.__socket=self.__context.socket(PUSH)
		self.__current_connection=None

	def connect(self,target_address,target_port):
		self.__socket.connect("tcp://%s:%d"%(target_address, target_port))
		pass

	def dis_connect(self, target_address, target_port):
		self.__socket.disconnect("tcp://%s:%d"%(target_address, target_port))
		pass

	def send(self,json_content):
		self.__socket.send_json(json_content)
		pass
	pass

class zmq_io_gateway(component_base):
	'''
	zmq网络模块的入口和出口
	'''
	def __init__(self,in_port,callback_entrance=None,binding_instance=None):
		'''指定输入端口号，整数
		指定回调函数入口
		指定持有这个端口的实例
		'''
		super(zmq_io_gateway, self).__init__(binding_instance)
		self.sender=zmq_send_connection()
		platform_category=binding_instance._environment_pack['current_platform_info']['current_system_category']
		self.lan_ip=get_local_ip(platform_category)

		if callback_entrance:
			self.listener=zmq_listen_connection(in_port,callback_entrance)
		pass
	pass