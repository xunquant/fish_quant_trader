# encoding: UTF-8
from __future__ import division
from PyQt4.QtCore import QTimer,Qt

from datetime import datetime

class my_timer(QTimer):
	def __init__(self,timeout_moment=None,timeout_task=None,repeat_interval=None,**kwargs):
		super(my_timer, self).__init__()

		self.__on_time_task=timeout_task
		self._arguments=kwargs
		self.timeout.connect(self.time_out_task, Qt.QueuedConnection)

		if timeout_moment and timeout_task:#如果指定了要定时做什么任务，就绑定之
			self.setSingleShot(True)#单次触发

			if timeout_moment.__class__.__name__ != 'datetime':
				print '定时器输入类别应该为datetime'
				return
			current_moment=datetime.now()
			if current_moment>timeout_moment:
				print('定时器触发时刻已经在当前时刻之前')
				return
			from_now2timeout=timeout_moment-current_moment
			self.start(1000*from_now2timeout.total_seconds())
			pass

		if repeat_interval and timeout_task:#如果指定了重复周期
			self.setSingleShot(False)
			repeat_interval.total_seconds()
			self.start(repeat_interval.total_seconds()*1000)
			pass
		pass

	def time_out_task(self):
		next_time_parameter=self._arguments['kwargs']

		if next_time_parameter:
			self.__on_time_task(next_time_parameter)
		else:
			self.__on_time_task()

		pass
	pass