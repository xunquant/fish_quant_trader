# -*- coding: utf-8 -*-

from program_top.components.standalone_working_class import standalone_working_class


class working_type_base(standalone_working_class):
	'''
	def __register_self(self):
		if self.__class__.__name__ =='background_hub':#如果自己就是background_hub类，则注册之
			stdafx.background_hub_ref=self
		pass
	'''

	def __init__(self,environment_pack):
		super(working_type_base, self).__init__(environment_pack)
		pass

	pass