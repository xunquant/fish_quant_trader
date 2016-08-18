# -*- coding: utf-8 -*-

from multiprocessing import Process
from zmq.eventloop.ioloop import IOLoop
from program_top.utilities.environment_and_platform import get_current_environment_pack

def main(start_script_file,running_class_def=None):
	'''主函数，传入开始执行的主函数，然后以指定的类作为起始工作实例，为单实例机器的程序入口'''
	current_environment_pack=get_current_environment_pack(start_script_absolute_filename=start_script_file)
	if running_class_def:
		current_working_instance=running_class_def(current_environment_pack)
		#print id(current_working_engine),'这里是主进程'



	IOLoop.instance().start()
	pass

class my_engine(Process):
	'''
	进程引擎，接受socket监听作为事件循环，发出请求的时候发起连接
	初始化确定本进程的执行参数，包括平台，python版本
	'''
	def __init__(self,working_type,environment_pack):
		super(my_engine, self).__init__()
		self.__environments=environment_pack
		self.__working_type=working_type
		self.__working_instance=None
		self.start()
		pass

	def run(self):
		#print id(self),'这里是子进程'
		self.__working_instance=self.__working_type(self.__environments)
		IOLoop.instance().start()
		pass
	pass

def load_instances():
	pass