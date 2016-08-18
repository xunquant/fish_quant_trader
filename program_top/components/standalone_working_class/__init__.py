# -*- coding: utf-8 -*-
import json
import os
from csv import DictReader

from program_top.components import component_base
from program_top.components.zmq_io_interface import zmq_io_gateway
from program_top.utilities.csv_and_json_serialisation import temperarily_load_a_local_json
from program_top.utilities.ip_and_socket import scan_available_ports_then_return
from program_top.utilities.my_dir import make_ever_dir

class standalone_working_class(component_base):
	'''
	独立工作类实例
	'''

	def __init__(self,environment_pack):
		super(standalone_working_class, self).__init__()
		self._environment_pack=environment_pack#环境变量包

		self.__path_initialisation()
		self.__port_and_loop_initilisation()
		pass

	def __port_and_loop_initilisation(self):
		'''端口和消息循环入口初始化'''
		port_for_listening=scan_available_ports_then_return(self._environment_pack['current_platform_info']['current_system_category'])

		self._io_gateway=zmq_io_gateway(port_for_listening, self.request_in, self)
		self._io_gateway.listening_port=port_for_listening
		pass

	def __path_initialisation(self):
		'''
		路径初始化
		'''
		instance_config_path=self._environment_pack['runtime_paths']['config_file_dir']+self.__class__.__name__+os.sep
		instance_resource_path=self._environment_pack['runtime_paths']['resource_dir']+self.__class__.__name__+os.sep
		instance_input_path=self._environment_pack['runtime_paths']['input_dir']+self.__class__.__name__+os.sep
		instance_buffer_path=self._environment_pack['runtime_paths']['buffer_dir']+self.__class__.__name__+os.sep
		insance_ouput_path=self._environment_pack['runtime_paths']['output_dir']+self.__class__.__name__+os.sep
		instance_extension_path=self._environment_pack['runtime_paths']['extension_dir']+self.__class__.__name__+os.sep

		instance_config={'config_file_dir': instance_config_path,
						 'resource_dir':instance_resource_path,
						 'input_dir':instance_input_path,
						 'buffer_dir':instance_buffer_path,
						 'ouput_dir':insance_ouput_path,
						 'extension_dir':instance_extension_path
						 }

		for each_dir in instance_config.values():
			make_ever_dir(each_dir)

		self._environment_pack['instance_config']=instance_config

		config_filename=self._environment_pack['instance_config']['config_file_dir']+'config.csv'

		if os.path.isfile(config_filename):
			self._load_business_config(config_filename)



		pass

	def _load_business_config(self, filename):
		'''加载配置文件'''

		is_there_config_file=(os.path.isfile(filename) and filename.endswith(".csv"))

		if not is_there_config_file:
			return is_there_config_file

		with open(filename, mode='rt') as file_handle:
			csv_contents=DictReader(file_handle)
			for each_row in csv_contents:
				self._business_config=each_row
				return is_there_config_file
				pass
			pass

		pass

	def _load_multiline_csv(self, filename, target_column=None):#读取多行csv文件
		return_list=[]
		if os.path.isfile(filename) and filename.endswith(".csv"):#如果文件存在并且以csv结尾
			with open(filename, mode='rt') as file_handle:
				csv_contents=DictReader(file_handle, fieldnames=target_column)
				for each_row in csv_contents:
					return_list.append(each_row)
					pass
				pass
			pass
		return return_list

	def _write_logs(self, string_list):#写日志文件
		a=type(string_list).__name__

		target_log=[str(id(self))]

		if a=='str':
			target_log.append(string_list)
			utilities.write_log(target_log)
		else:
			utilities.write_log(string_list)
		pass

	def _load_if_exist(self, absolute_filename):#如果存在此文件就读取，否则返回none
		if os.path.isfile(absolute_filename):
			with open(absolute_filename, mode='r') as file_load:
				return json.load(file_load)
			pass
		pass

	def _save_data(self, absolute_filename, target_data_in_dict):#将字典数据存入json文件
		if os.name=='nt':#如果是windows系统
			absolute_filename=absolute_filename.decode('utf-8').encode('gb18030')

		with open(absolute_filename, mode='w') as file_dump:
			file_dump.write(json.dumps(target_data_in_dict))
			file_dump.close()
			pass
		pass

	def _inform_ready(self):
		'''当自己的初始化完成后，调用此函数通知整个工作网络，自己的IP和端口是多少，并加入自己的环境变量'''

		config_filename=self._environment_pack['instance_config']['config_file_dir']+'lan_ip_config.json'

		if os.path.isfile(config_filename):
			ip_info=temperarily_load_a_local_json(config_filename)
			self._io_gateway.sender.send()

			pass





		pass
	pass