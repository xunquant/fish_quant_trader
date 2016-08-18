# encoding: UTF-8
import os
from datetime import timedelta,datetime

from pandas import DataFrame
from program_top.my_event_base import custom_events
from program_top.my_event_base.custom_events import curl_certain_type_raw_data_request
from program_top.standalone_working_class.working_type_base.front_end_base.analysis_project_base import analysis_project_base

from program_top.components.standalone_working_class.working_type_base.backend_interface_base.elasticsearch_interface_base import successful_reservation,cancel_reservation, failed_reservation
from program_top.utilities.my_datetime import derby_elasticsearch_date_format
from program_top.utilities.my_dir import make_ever_dir

def repeat_test(string_target=None):

	if string_target:
		print 'repeating',string_target,datetime.now()
	else:
		print 'repeating'
	pass

class curl_perflog_of_certain_type(analysis_project_base):
	"""
	拉取指定类型的日志，并缓存到相应のoutput文件夹中
	"""
	def __init__(self, target_log_type=None):
		super(curl_perflog_of_certain_type, self).__init__()

		self._output_directory_suc=self._output_directory+'successful_reservation'+os.sep
		self._output_directory_failed=self._output_directory+'failed_reservation'+os.sep
		self._output_directory_cancel=self._output_directory+'cancel_reservation'+os.sep
		make_ever_dir(self._output_directory_suc)
		make_ever_dir(self._output_directory_failed)
		make_ever_dir(self._output_directory_cancel)
		self._target_data_type=target_log_type
		self._load_supplier_channel_pairs(self._resource_directory+'supplier_distributor_pairs.csv')
		self._register_event_and_processor(custom_events.check_data_response, self._got_data_back)
		pass

	def _upstream_ready_noticed(self,ready_to_work_event):
		'''接口类准备好，可以开始定期查数据'''

		self._data_interface=ready_to_work_event.event_content['sender']
		repeat_interval=timedelta(days=int(self._business_config['day']), hours=int(self._business_config['hour']),
								  minutes=int(self._business_config['minute']), seconds=int(self._business_config['second']))
		self._periodically_do(repeat_interval,self.__curl_all)
		pass

	def __curl_all(self):
		'''拉所有数据'''
		self._query_certain_type_perf_log(hotel_name=self._suppliers, target_log_type=successful_reservation)
		self._query_certain_type_perf_log(hotel_name=self._suppliers, target_log_type=cancel_reservation)
		self._query_certain_type_perf_log(hotel_name=self._suppliers, target_log_type=failed_reservation)
		pass

	def _got_data_back(self,event_with_data):
		current_data_content=event_with_data.event_content
		data_pack=current_data_content['data_content']
		self.__save_data_by_date_on_each_supplier(data_pack)
		pass

	def __save_data_by_date_on_each_supplier(self, each_day):
		if not isinstance(each_day,dict):
			self._write_logs("不是传入数据格式有误，本应是字典")
			return

		if (not each_day.__contains__('data') )or(not isinstance(each_day['data'],list)) or (not each_day['data'].__len__()):
			return

		process_original=each_day['data'][0]['process_original']
		process_result=each_day['data'][0]['process_result']
		if process_original.startswith('B') and process_result.startswith('S'):
			current_output_dir=self._output_directory_suc
		if process_original.startswith('B') and process_result.startswith('F'):
			current_output_dir=self._output_directory_failed
		if process_original.startswith('C'):
			current_output_dir=self._output_directory_cancel

		date_string=each_day['date'].strftime(derby_elasticsearch_date_format)
		supplier_name=each_day['supplier']

		filename=current_output_dir+'_'.join([supplier_name, date_string+'.csv'])
		today_panel=DataFrame(each_day['data'])
		today_panel.to_csv(filename)
		pass

	def _response_finish_informed(self,responsing_event):
		requesting_event_id=responsing_event.event_content['answer_to_request_id']
		if self._query_in_queue.__contains__(requesting_event_id):
			self._query_in_queue.pop(requesting_event_id)
		downstream_instance_ref=self._check_instance_ref('generate_top_hotel_in_each_channels')
		self._ready_to_work(downstream_instance_ref)
		pass

	def _query_certain_type_perf_log(self, hotel_name=None, target_date=None, target_log_type=None):
		'''
		查询特定类型的订单数据
		'''
		current_query=curl_certain_type_raw_data_request(requesting_instance=self, hotel_name=hotel_name, target_date=target_date, target_perf_type=target_log_type, replica=None)
		self._query_in_queue[current_query.event_content['request_id']]=current_query
		self._data_interface.take_in_event(current_query)

class curl_all_successful_reservation(curl_perflog_of_certain_type):
	'''
	拉取所有订单，并缓存到相应の文件夹中
	'''
	def __init__(self):
		super(curl_all_successful_reservation, self).__init__(target_log_type=successful_reservation)
		pass

class curl_canceled_reservation(curl_perflog_of_certain_type):
	'''
	拉取取消的订单，缓存到相应文件夹中
	'''
	def __init__(self):
		self._target_data_type=cancel_reservation#要取的目标数据类别
		super(curl_canceled_reservation, self).__init__(target_log_type=cancel_reservation)

		pass
	pass


class curl_reservation_failure(curl_perflog_of_certain_type):
	def __init__(self):
		self._target_data_type=failed_reservation#要取的目标数据类别
		super(curl_reservation_failure, self).__init__(target_log_type=self._target_data_type)

		pass
	pass