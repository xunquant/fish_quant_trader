# encoding: UTF-8
from datetime import datetime

import pandas
from program_top.data_classes.my_table import my_table
from program_top.standalone_working_class.working_type_base.front_end_base.analysis_project_base.curl_reservation_of_certain_type import curl_perflog_of_certain_type
from program_top.stdafx import my_path,os

import program_top.utilities.my_dir
from program_top.components.standalone_working_class.working_type_base.front_end_base.analysis_project_base.models_base import models_base
from program_top.utilities import my_pandas
from program_top.utilities.my_datetime import derby_elasticsearch_date_format
from program_top.utilities.single_layer_map import single_layer_map

class generate_top_hotel_in_each_channels(models_base):
	'''
	生成酒店绩效数据，列出各个渠道内各个酒店的绩效，列出不考虑渠道的各个酒店绩效
	'''
	def __init__(self):
		super(generate_top_hotel_in_each_channels, self).__init__()
		raw_data_stem_path=my_path.output_path+curl_perflog_of_certain_type.__name__+os.sep
		self._reservation_data_path=raw_data_stem_path+self._business_config['book_path_relative_name']+os.sep
		self._failed_data_path=raw_data_stem_path+self._business_config['failed_reservation_relative_name']+os.sep
		self._canceled_data_path=raw_data_stem_path+self._business_config['cancel_path_relative_name']+os.sep
		pass

	def _upstream_ready_noticed(self,ready_to_work_event):
		'''收到上游类发来通知就做统计'''
		self.__do_stat()
		pass

	def __do_stat(self):
		'''定期做统计'''
		failed_reservs=program_top.utilities.my_dir.browse_dir(self._failed_data_path)
		extracted_failed_order=pandas.concat([self.__get_needed_data_from_each_file(each_file) for each_file in failed_reservs])

		#cancal_reservs=utilities.browse_dir(self._canceled_data_path)

		ordered_reservs=program_top.utilities.my_dir.browse_dir(self._reservation_data_path)
		#ordered_reservs.extend(cancal_reservs)

		extracted_mix_reserve=[self.__get_needed_data_from_each_file(each_file) for each_file in ordered_reservs]
		total_reserve_with_cancel=pandas.concat(extracted_mix_reserve)#没有扣除cancel数据的

		total_reserve_with_cancel.to_csv(self._output_directory+'total_reserve_raw.csv')
		extracted_failed_order.to_csv(self._output_directory+'total_failure_raw.csv')

		reservation_tables=self.__generate_tables(total_reserve_with_cancel,'pure_reservation')
		failed_order_tables=self.__generate_tables(extracted_failed_order, 'failed_order')

		normalised_tables=[]
		for i in xrange(reservation_tables.__len__()):
			normalised_tables.append(self.__get_diveded_forms(failed_order_tables[i],reservation_tables[i],'sum_count'))
			pass

		self.__print_forms(normalised_tables)
		self.__print_forms(reservation_tables)
		self.__print_forms(failed_order_tables)

		log_string='定期订单统计完成'
		self._write_logs(log_string)
		down_stream_ref=self._check_instance_ref('failure_rate_and_caution_score_analysis')
		self._ready_to_work(down_stream_ref)
		pass

	def __get_diveded_forms(self,divided,dividing,value_key):
		temp_result=divided.form_content.divide(dividing.form_content,axis=[0,1],level=None, fill_value=None)
		new_column_name= divided.column_name if divided.column_name==dividing.column_name else None
		new_index_name=divided.index_name if divided.index_name==dividing.index_name else None
		return my_table('failure_rate', column_name=new_column_name, index_name=new_index_name, existing_pivoted_table=temp_result)

	def __print_forms(self,data_dicts):
		for each in data_dicts:
			each.output_form(self._output_directory)
			pass
		pass

	def __generate_tables(self,raw_record_frame,data_content_name):
		table_list=[]
		table_list.append(my_table(data_content_name, 'hotel_supplier', 'supplier', raw_record_frame=raw_record_frame))
		table_list.append(my_table(data_content_name, 'channel', 'supplier', raw_record_frame=raw_record_frame))
		table_list.append(my_table(data_content_name, 'hotel_supplier', 'channel', raw_record_frame=raw_record_frame))
		return table_list

	def __get_needed_data_from_each_file(self,data_filename):
		'''
		从每个文件提取需要的数据
		'''

		current_dataframe=pandas.DataFrame.from_csv(data_filename)
		each_day_record=self.__extract_interested_data_from_current_dataframe(current_dataframe)
		return each_day_record

	def __extract_interested_data_from_current_dataframe(self,target_dataframe):
		'''
		每个模型不相同，需要什么数据就从数据文件里取什么数据，在这个函数里面定义取数据の代码
		'''
		if not target_dataframe.size:#如果什么数据都没有
			return

		return_date_func=lambda x:(pandas.to_datetime(x).date() if isinstance(x,str) else None)
		process_info=target_dataframe['process_original'].unique()[0]#过程名称
		record_sign=-1 if process_info.__contains__('ancel') else 1#交易记录的符号，取消订单为-1，订单为1
		target_dataframe['sum_count']=target_dataframe['order_count_per_record']*record_sign
		target_dataframe['date_stamp']=target_dataframe.timestamp.apply(return_date_func)
		selected_sub=target_dataframe.ix[:,['channel','supplier', 'hotel_supplier', 'date_stamp', 'sum_count']]#选取特定的字段
		grouped=my_pandas.dataframe_element_wise_prepare(selected_sub, 'sum_count')
		new_test=my_pandas.dataframe_index_back_to_key(grouped)
		return new_test

	def _response_finish_informed(self,responsing_event):
		super(generate_top_hotel_in_each_channels, self)._response_finish_informed(responsing_event)

	def __scan_intermediate_data_folder(self,file_lists):
		map(self.__each_file_handler,file_lists)
		temp_panel=pandas.DataFrame(self._data_buffers)
		pivoted_test_1=pandas.pivot_table(data=temp_panel,values=['room_count'],index=['channel_name','hotel_name'],columns=['date'],fill_value=0)
		group_regardless_date=temp_panel.groupby(['channel_name','hotel_name'])
		x=group_regardless_date.sum()
		x=x.room_count
		x_table=pandas.pivot_table(data=x,index=['channel_name'],columns=['hotel_name'],fill_value=0)
		temp_panel.pop('date')
		pivoted_test_2_without_date=pandas.pivot_table(temp_panel,values=['room_count'],index='channel_name',columns=['hotel_name'],fill_value=0,aggfunc='sum').T
		pivoted_test_2_without_date.to_csv('pivoted_test_2_without_date.csv',mode='w')
		temp_panel.pop('channel_name')
		pivoted_test_3_with_only_hotel=pandas.pivot_table(temp_panel,values=['room_count'],index=['hotel_name'],fill_value=0,aggfunc='sum')
		pivoted_test_3_with_only_hotel.to_csv('pivoted_test_3_with_only_hotel.csv')

		print x
		pivoted_test_1.to_csv('pivoted_test_1.csv',mode='w')
		group_regardless_date.to_csv('grouped_1.csv',mode='w')


		pass

	def __extract_from_each_row_line(self,each_line_row):
		return each_line_row['process_duration']!='room_cnt'

	def __each_record_processing(self,each_record,actual_date):
		each_record['date']=actual_date
		each_record.pop('order_count')
		each_record.pop('adult')
		each_record.pop('process_duration')
		each_record['room_count']=int(float(each_record['room_count']))
		return each_record

	def __each_file_handler(self,current_file):
		current_file_name=program_top.stdafx.my_path.output_path+current_file
		raw_lines=self._load_multiline_csv(current_file_name,['channel_name','hotel_name','adult','order_count','process_duration','room_count'])
		raw_lines=filter(self.__extract_from_each_row_line,raw_lines)

		temp_filenames=current_file.split('_')
		actual_date=datetime.strptime(temp_filenames[1],derby_elasticsearch_date_format).date()
		individual_record_list=single_layer_map(self.__each_record_processing, raw_lines, actual_date).result
		self._data_buffers.extend(individual_record_list)
		pass
	pass