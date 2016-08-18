# encoding: UTF-8
from StringIO import StringIO
from datetime import datetime
from pycurl import Curl

import json
import os
import program_top.data_classes
import program_top.data_classes.derby_perflog
import program_top.stdafx.my_path
import requests
from program_top.data_classes.derby_perflog import extract_derby_book_from_each_dict_perf_log
from program_top.my_event_base import custom_events
from program_top.standalone_working_class.working_type_base import working_type_base

import program_top.utilities.my_datetime
import program_top.utilities.my_dir
from program_top.utilities.my_datetime import derby_elasticsearch_date_format

class elastic_interface_base(working_type_base):

	def __ready_action(self):
		self._ready_to_work(self._check_instance_ref('curl_perflog_of_certain_type'))


	def __init__(self):
		super(elastic_interface_base, self).__init__()
		self._data_availability_panel={}
		self._hosts_address=self._business_config['elasticsearch_address']
		self._date_back_range()
		self.__current_processing_function=None
		self._register_event_and_processor(custom_events.curl_certain_type_raw_data_request,
										   self.__curl_all_perflog_of_hotels_in_set)
		self.__ready_action()

	def _get_curl_buffer_filename(self,target_url,commit_date=datetime.today()):
		'''
		返回curl指令结果应该缓存成的文件名
		'''
		return program_top.utilities.my_dir.string2filename(target_url)

	def _curl_a_post(self,post_url,query_target_dict):
		'''
		:param post_url:发出连接的url
		:type post_url: 字符串
		:param query_target_dict:查询目标数据类别
		:type query_target_dict: 字典
		:return: 返回结果
		:rtype:
		'''
		query_json_string=json.dumps(query_target_dict)
		response=requests.post(post_url,data=query_json_string)
		results=json.loads(response.text)
		return results

	def _curl_a_link(self, target_url,post_target, commit_date=None):
		'''
		解析一个地址，返回一个字典，从其中可以读取json字符串の内容，相当于curl get指令，如果这个请求的结果在今天的缓存当中已经有了，则从缓存中取，不从elastic里面再重复读取
		'''

		buffer = StringIO()
		c = Curl()
		c.setopt(c.URL,target_url)
		c.setopt(c.WRITEDATA, buffer)
		c.perform()
		c.close()

		load_target=json.loads(buffer.getvalue())

		return load_target
		pass

	def _map_stem(self, stem_url=None):
		target_link=(stem_url if stem_url else self._hosts_address)+'_mapping'
		return self._curl_a_link(target_link,datetime.today())

	def _search_all(self, stem_url=None):
		'''
		列出主干下所有的可获取条目，使用search
		'''
		target_link=(stem_url if stem_url else self._hosts_address)+'_search'
		testing_one=self._curl_a_link(target_link)
		pass

	def _post_data_back_to_model(self, original_command_event, event_data, is_last=None):
		'''
		数据回传给模型
		'''
		current_checked_data_event=custom_events.check_data_response(sender_instance=self,data_content=event_data, requesting_event=original_command_event, is_last=is_last)
		receiver=original_command_event.event_content['sender']
		receiver.take_in_event(current_checked_data_event)
		pass

	def _list_all_index(self):
		return self._curl_a_link(self._hosts_address+'_stats',datetime.today().date())['indices']

	def _date_back_range(self):
		'''
		找数据回溯的射程(从当日开始回溯，能回溯到哪一天的数据)
		'''
		indices_list=self._list_all_index()
		for each_index in indices_list:
			current_index=each_index
			current_index_info=current_index.split('-')
			if current_index_info.__len__()<=2:
				continue
				pass

			current_available_date=datetime.strptime(current_index_info[-1],
													 program_top.utilities.my_datetime.derby_elasticsearch_date_format).date()
			current_index_channel_name=current_index_info[-2]
			if not self._data_availability_panel.has_key(current_index_channel_name):#如果已有这个渠道的日期列表
				self._data_availability_panel[current_index_channel_name]=set()
			self._data_availability_panel[current_index_channel_name].add(current_available_date)
			pass
		pass

	def __get_curl_url(self,supplier,date):
		'''
		根据搜索供应商和日期确定要搜索的url
		'''

		date_string=date.strftime(derby_elasticsearch_date_format)
		each_curl_tail_description='res/_search?size=100000'
		perf='/perf_'
		each_curl_head_section='http://support.derbysoft.com/elasticsearch/derbysoft-'
		url=each_curl_head_section+supplier+'-'+date_string+perf+supplier+each_curl_tail_description
		#url = 'http://support.derbysoft.com/elasticsearch/derbysoft-bico-20160331/perf_bicores/_search?size=100000'
		return url

	def __curl_all_perflog_of_hotels_in_set(self, curl_command):
		'''
		取得酒店集合的订单
		'''

		event_content=curl_command.event_content
		if event_content.__contains__('processing_function'):
			self.__current_processing_function=event_content['processing_function']

		for each_supplier in event_content['hotel_name']:
			self.__curl_all_perflog_of_one_supplier(curl_command, each_supplier)
			pass

		self.__current_processing_function=None#数据处理函数重新置为none

		self._response_finished(request_event=curl_command)
		print(event_content['sender'].__class__.__name__+'数据已经查询完毕')

		#my_engine(generate_top_hotel_in_each_channels)

		pass

	def __curl_one_supplier_one_date_all_perflog(self, supplier_name, target_date,target_log_type):
		'''
		拉取一个酒店公司一天的成功的订单数据
		'''

		target_url=self.__get_curl_url(supplier_name,target_date)
		perflog_result=self._curl_a_post(target_url,target_log_type)
		if (not perflog_result.__contains__('hits')) or (not perflog_result['hits'].__contains__('hits')):
			log_string=supplier_name+target_date.strftime(derby_elasticsearch_date_format)+'无记录'
			self._write_logs(log_string)
			return []

		temp_result=perflog_result['hits']['hits']
		derby_perflog_list=map(extract_derby_book_from_each_dict_perf_log,temp_result)

		if not derby_perflog_list:
			return derby_perflog_list
		if derby_perflog_list.__len__()>=100000:
			self._write_logs(supplier_name, target_date.strftime(derby_elasticsearch_date_format),'警告，本次查询结果条数有可能多于100000')

		return derby_perflog_list

	def __curl_all_perflog_of_one_supplier(self, curl_command, supplier_name=None, target_date=None):#取得单个酒店的订单
		result_list=list()
		if not self._data_availability_panel.__contains__(supplier_name):
			return result_list

		output_path=program_top.stdafx.my_path.output_path+curl_command.event_content['sender'].__class__.__name__+os.sep
		target_data_type=curl_command.event_content['target_perf_type']

		dates_available_list_of_current_supplier=self._data_availability_panel[supplier_name]

		if not target_date:#如果没有指名要查询哪一天的，就查询所有
			while len(dates_available_list_of_current_supplier):#只要集合不为空
				current_target_date=dates_available_list_of_current_supplier.pop()
				current_target_date_string=current_target_date.strftime(derby_elasticsearch_date_format)
				today_raw_filename=output_path+supplier_name+'_'+current_target_date_string+'.csv'
				if os.path.isfile(today_raw_filename):#如果今天同一家supplier的已经读取，则跳过
					continue
				temp_result=self.__curl_one_supplier_one_date_all_perflog(supplier_name, current_target_date,target_log_type=target_data_type)
				data_package={'supplier':supplier_name,'date':current_target_date,'data':temp_result}
				self._post_data_back_to_model(curl_command,data_package)
				pass



			pass
		return result_list