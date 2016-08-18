# -*- coding: utf-8 -*-

class component_base(object):
	'''
	组件，非独立占据一个进程的组装配件，组件不具备独立的各种环境变量文件夹，只从request_in成员输入dict指令，它的子类standalone某某才有独立的环境变量，独占一个进程
	'''
	def __init__(self,parrent_instance=None):
		super(component_base, self).__init__()
		if parrent_instance:
			self._binding_instance=parrent_instance
			self._environment_pack=parrent_instance._environment_pack
		self.__event_dict={}#储存事件类别和对应处理消息的函数的字典
		pass

	def request_in(self,command_to_component):
		'''对本组件的事件入口，必须重载才能调用'''
		event_type=command_to_component.event['event_type']

		if self.__event_dict.__contains__(event_type):
			return self.__event_dict[event_type](command_to_component.event)
		else:
			print '事件类别%s未注册'%(event_type)
			return None
		pass

	def _register_event_and_processor(self,event_type_name,processing_funtion):
		'''将事件和对应的处理函数注册'''

		if not self.__event_dict.__contains__(event_type_name):#如果本类事件之前还没有被注册
			self.__event_dict[event_type_name]=processing_funtion
		pass

	def _deregister_event_and_processor(self, event_type_name):
		'''将事件和对应的处理函数注销'''
		if self.__event_dict.__contains__(event_type_name):
			self.__event_dict.pop(event_type_name)
		pass
	pass