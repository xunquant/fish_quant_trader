# -*- coding: utf-8 -*-

from program_top.components.standalone_working_class import standalone_working_class

class process_manager(standalone_working_class):
	'''
	主进程的主要工作实例，接收外部tcp传入的消息，保存整个工作网络的参数和环境变量，当时间到时向订阅定时器事件的进程发出消息
	'''

	def __init__(self,environment_pack=None):#如有环境变量信息则传入
		super(process_manager, self).__init__(environment_pack)

		self.__address_table={}#地址表，各个类实例的名称，以及它们在本网络内的地址，地址格式以tcp://ip:port为准，接收到查询请求的时候返回当前的地址表给需要此表的工作实例
		pass
	pass