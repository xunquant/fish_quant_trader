# encoding: UTF-8
import os

import pandas
from pandas import DataFrame, pivot_table
from program_top.ghr_interface import ghr_interface
from program_top.stdafx import my_path
from program_top.widgets.plain_chart import scattered_xy_chart, pie_chart, bar_chart
from program_top.widgets.surface_3d_figure import surface_3d_figure

import program_top.utilities.my_dir
from generate_top_hotel_in_each_channels import generate_top_hotel_in_each_channels
from ..models_base import models_base

hotel_searcher_ref=ghr_interface()

class failure_rate_and_caution_score_analysis(models_base):
	'''
	1.根据失误总数据、订单总数据，生成各个酒店/渠道/供应商的失误率数据
	2.根据每个酒店的订单计数、失误率，计算每个酒店的失误报警分数(caution_score，公式为失误率×power(指数底，订单数)，其中指数底是一个可以优化的参数)
	3.使用supplier对channel的失误率，生成海拔图
	4.对所有酒店的失误率数据，订单总量数据，报警分数数据，做cut分类/分组，然后对各组做饼图和条图
	5.对所有酒店的失误率和订单总量做x,y散点图。
	6.对失误率和报警分数，找出极值出现在哪家酒店
	'''

	def __init__(self):
		super(failure_rate_and_caution_score_analysis, self).__init__()
		self._caution_base_number=int(self._business_config['caution_base']) ** int(self._business_config['caution_base_exponent'])#警告指数函数的底
		self._caution_threshold=int(self._business_config['warning_threshold'])#警告指数函数报警的阈值
		self._input_directory=my_path.output_path+generate_top_hotel_in_each_channels.__name__+os.sep
		pass

	def _upstream_ready_noticed(self,ready_to_work_event):
		self.__do_the_stats()
		pass

	def _clear_up_before_data_update(self):
		'''
		每次计算数值前要初始化类实例的数据
		'''
		self._reservation_panels={}
		self._reservation_importance_panels={}
		self._failure_panels={}
		self._failure_rate_panels={}
		self._caution_score_panel={}
		self._double_key_failure_panels={}
		self._double_key_failure_rate_panels={}
		self._double_key_reservatoin_panels={}
		self._double_key_importance_panels={}
		self._double_key_caution_score_panel={}

		program_top.utilities.my_dir.clear_dir_tree(self._output_directory)

		pass

	def __do_the_stats(self):
		'''周期性调用'''

		file_list=program_top.utilities.my_dir.browse_dir(self._input_directory, '.csv')

		fail_file_filter=lambda x: (x.__contains__('fail') and x.__contains__('total'))
		pure_file_fileter=lambda x: (x.__contains__('reserve') and x.__contains__('total'))

		fail_file_list=filter(fail_file_filter, file_list)
		pure_file_list=filter(pure_file_fileter, file_list)

		self._clear_up_before_data_update()

		self._failure_total_data=DataFrame.from_csv(fail_file_list[0])
		self._reservation_total_data=DataFrame.from_csv(pure_file_list[0])
		self._total_reservation_count=self._reservation_total_data.sum(numeric_only=True).values.tolist()[0]

		keys_of_interest=['supplier','channel','hotel_supplier']
		value_key='sum_count'
		total_supplier_lists=self._reservation_total_data['supplier'].unique().tolist()
		self._active_hotel_counts=hotel_searcher_ref.get_active_hotel_lists(total_supplier_lists)

		self._get_two_key_vs_failure_rate(keys_of_interest[0], keys_of_interest[1], value_key=value_key)
		self._get_two_key_vs_importance_panel(keys_of_interest[0], keys_of_interest[1], value_key=value_key)
		self._output_two_key_vs_caution_score(keys_of_interest[0], keys_of_interest[1], value_key=value_key)

		#self._output_altitude_plot(keys_of_interest[0], keys_of_interest[1], self._double_key_failure_rate_panels[keys_of_interest[0], keys_of_interest[1]])

		for each_key in keys_of_interest:
			self._output_failure_rate_of_each_key(each_key, keys_of_interest, value_key)
			self._get_reservation_importance(each_key,keys_of_interest,value_key)
			self._output_caution_score_of_each_key(each_key, keys_of_interest, value_key)
			pass

		#self._output_failure_rate_vs_reservation_scattered_point_plot(keys_of_interest[2])
		#self._output_caution_score_vs_reservation_importance_scattered_point_plot(keys_of_interest[2])
		#self._cut_data_into_categorical_group(keys_of_interest[2],'failure_rate',50,self._failure_rate_panels[keys_of_interest[2]])
		#self._cut_data_into_categorical_group(keys_of_interest[2],'caution_score',50,self._caution_score_panel[keys_of_interest[2]])
		self._write_logs('订单失误和警告分数统计完成')
		from program_top.process_engine import my_engine
		from program_top.components.standalone_working_class.working_type_base import s3_gate_uploader
		my_engine(s3_gate_uploader)#创建一个s3上传数据的实例
		pass

	def _find_max_index_in_1d_panel(self,target_panel):
		test_value=target_panel.idxmax()

		data_type=target_panel.__class__
		original_is_series=(target_panel.__class__==pandas.Series)
		if data_type == pandas.Series:
			new_instance=pandas.Series(test_value,index=['max_value_index'])
			new_panel=target_panel.append(new_instance)
			return new_panel
			pass

		if data_type== pandas.DataFrame:

			print data_type.__name__
			pass
		pass

	def _output_failure_rate_vs_reservation_scattered_point_plot(self, key_name):
		'''
		绘制各个key对应的订单数量和失误率的散点图
		'''
		relative_filename='reservation_count_vs_failure_rate_scattered'
		full_filename=self._output_directory+relative_filename+'.png'
		y_data=self._failure_rate_panels[key_name]
		x_data=self._reservation_panels[key_name]
		scattered_xy_chart(full_filename,'reservation_count','failure_rate',x_data,y_data)
		pass

	def _output_caution_score_vs_reservation_importance_scattered_point_plot(self, key_name):
		relative_filename='caution_score_vs_reservation_importance_scattered'
		full_filename=self._output_directory+relative_filename+'.png'
		x_data=self._reservation_importance_panels[key_name]
		y_data=self._caution_score_panel[key_name]

		scattered_xy_chart(full_filename,'reservation_importance','caution_score',x_data,y_data)
		pass

	def _cut_data_into_categorical_group(self, index_key, content_key, group_count, target_dataframe):
		'''
		需求4,：对数据做分组切片，输入的数据必须是1维的， 输入分组的组数
		'''
		cutted,bins=pandas.cut(target_dataframe,group_count,retbins=True)
		new_grouped_frame=target_dataframe.groupby(cutted)
		k_size=new_grouped_frame.size()

		pie_plot_instance=pie_chart(self._output_directory+index_key+'_'+content_key,k_size)
		bar_chart_instance=bar_chart(self._output_directory+index_key+'_'+content_key,k_size)
		pass

	def _get_two_key_vs_importance_panel(self,key_x,key_y,value_key):
		self._double_key_reservatoin_panels[key_x,key_y]=pivot_table(self._reservation_total_data,index=key_x,columns=key_y,aggfunc='sum',values=value_key)
		self._double_key_importance_panels[key_x,key_y]=self._double_key_reservatoin_panels[key_x,key_y].div(self._total_reservation_count,axis=[0,1],level=None,fill_value=None)
		pass

	def _output_two_key_vs_caution_score(self, key_x, key_y, value_key):
		current_failure_rate=self._double_key_failure_rate_panels[key_x,key_y]
		current_reservation_importance=self._double_key_importance_panels[key_x,key_y]
		current_exponential=current_reservation_importance.rpow(self._caution_base_number, axis=[0,1], level=None, fill_value=None)
		current_caution_score=current_failure_rate.mul(current_exponential, axis=[0,1], level=None, fill_value=None)
		self._double_key_caution_score_panel[key_x,key_y]=current_caution_score
		current_caution_score.to_csv(self._output_directory+key_x+'_vs_'+key_y+'_caution_score.csv',mode='w')
		pass

	def _get_two_key_vs_failure_rate(self,key_x,key_y,value_key):
		failure_pivoted=pivot_table(self._failure_total_data,index=key_x,columns=key_y,aggfunc='sum',values=value_key,fill_value=None,dropna=False)
		reservation_pivoted=pivot_table(self._reservation_total_data,index=key_x,columns=key_y,aggfunc='sum',values=value_key,fill_value=None,dropna=False)
		failure_rate=failure_pivoted.div(reservation_pivoted,axis=[0,1], level=None, fill_value=None)
		self._double_key_failure_rate_panels[key_x,key_y]=failure_rate
		pass

	def _get_reservation_importance(self,key_name,all_keys,value_key):
		self._reservation_importance_panels[key_name]=self._reservation_panels[key_name].div(self._total_reservation_count, axis=0, level=None, fill_value=None)
		pass

	def _output_failure_rate_of_each_key(self, key_name, all_keys, value_key):
		'''
		需求1:算出失误率表格
		'''
		target_filename=self._output_directory+key_name+'_'+'failure_rate.csv'

		pivoted_table_failure=pivot_table(self._failure_total_data,values=value_key,index=[key_name],aggfunc='sum',fill_value=None,dropna=False)
		pivoted_table_reserve=pivot_table(self._reservation_total_data,values=value_key,index=[key_name],aggfunc='sum',fill_value=None,dropna=False)
		self._failure_panels[key_name]=pivoted_table_failure
		self._reservation_panels[key_name]=pivoted_table_reserve

		if os.path.isfile(target_filename):
			failure_rate_table=DataFrame.from_csv(target_filename)
			self._failure_rate_panels[key_name]=failure_rate_table
			return

		failure_rate_table=pivoted_table_failure.divide(pivoted_table_reserve,axis=0, level=None, fill_value=None)

		#failure_rate_table=self._find_max_index_in_1d_panel(failure_rate_table)

		failure_rate_table.to_csv(target_filename)
		self._failure_rate_panels[key_name]=failure_rate_table
		pass

	def _output_caution_score_of_each_key(self, key_name, all_keys, value_key):
		'''
		需求2:得出每个key的警告分数，目前设置警告对数底(_caution_base_number)为2，警告阈值(_caution_threshold)为1，计算公式为：错误率×power(警告指数底，订单总数)-警告阈值，大于0则报警，小于0忽略
		'''
		target_filename=self._output_directory+key_name+'_'+'caution_score.csv'

		if os.path.isfile(target_filename):
			current_caution_score=DataFrame.from_csv(target_filename)
			self._caution_score_panel[key_name]=current_caution_score
			return

		current_failure_rate=self._failure_rate_panels[key_name]
		current_reservation_importance=self._reservation_importance_panels[key_name]
		test_series=pandas.Series(current_failure_rate)
		current_exponential=current_reservation_importance.rpow(self._caution_base_number, axis=0, level=None, fill_value=None)
		current_caution_score=current_failure_rate.mul(current_exponential, axis=0, level=None, fill_value=None)
		self._caution_score_panel[key_name]=current_caution_score
		current_caution_score.to_csv(target_filename)
		pass

	def _output_altitude_plot(self, key_x, key_y, data_set):
		'''
		需求3：生成海拔图
		'''
		output_figure_filename=key_x+'_vs_'+key_y+'3d_surface.png'
		figure=surface_3d_figure(data_set,self._output_directory+output_figure_filename)
		pass

	pass