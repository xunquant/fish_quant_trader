# -*- coding: utf-8 -*-

'''事件系统使用以下字典来组合事件dict的各个字段，事件内不可包含，以下若干字段可以独一无二的指定一个事件'''

from program_top.utilities.container_operations import covering_merge_dicts
from program_top.utilities.my_datetime import my_date_time_microsec_format
import datetime

event_type={
	'event_type':None
}#事件基本字段：事件类别

sending_time={
	'sending_time':None
}#发送方发出事件的时间，设定成发送时刻datetime的字符串

sender_ip={
	'sender_ip':None
}#发送方的ip

receiver_ip={
	'receiver_ip':None
}#接收者的ip

receiver_port={
	'receiver_port':None
}#接收者的端口

class event_base(object):
	def __init__(self):
		'''构造一个基本事件，然后指定其创建的时间戳'''
		super(event_base, self).__init__()
		time_stamp=datetime.datetime.now().strftime(my_date_time_microsec_format)
		basic_event_instance=covering_merge_dicts([event_type, sending_time])
		basic_event_instance['sending_time']=time_stamp
		basic_event_instance['event_type']=self.__class__.__name__
		self.event=basic_event_instance
		pass
	pass

