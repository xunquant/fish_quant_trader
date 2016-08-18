# encoding: UTF-8

from datetime import datetime

import program_top.utilities.my_dir
from program_top.utilities.my_datetime import derby_elasticsearch_date_format
from program_top.my_event_base import custom_events
from ...front_end_base import front_end_base

#每一个研究目的创建一个研究项目实例，都从此继承
class analysis_project_base(front_end_base):
	def __init__(self):
		super(analysis_project_base, self).__init__(config_filename=None)
		self._query_in_queue={}
		self._register_event_and_processor(custom_events.check_data_response, self._got_data_back)

	def _load_supplier_channel_pairs(self,pair_filename):
		'''
		读取supplier和channel组合的文档
		'''
		supplier_channel_pairs_panel=self._load_multiline_csv(pair_filename)
		supplier_set=set()
		distributor_set=set()
		for each_pair in supplier_channel_pairs_panel:
			distributor_set.add(each_pair['Distributor'])
			current_supplier=each_pair['Supplier'].lower().replace(' ','')
			supplier_set.add(current_supplier)
			pass

		self._suppliers=supplier_set
		self._distributors=distributor_set
	def _got_data_back(self,event_with_data):
		pass

	def _get_data_filename_from_supplier_name_and_date(self,supplier_name,date):
		'''
		根据酒店公司の名称和日期取得对应文件的数据文件
		'''
		date_string=date.strftime(derby_elasticsearch_date_format)
		filename=self._output_directory+'_'.join([supplier_name, date_string+'.csv'])
		return filename

	def _get_supplier_name_and_data_from_data_filename(self,file_fullname):
		'''
		根据文件名取得日期和供应商信息
		'''
		relative_filename=program_top.utilities.my_dir.get_relative_filename_from_absolute(file_fullname)
		filename_info=relative_filename.replace('.csv','').split('_')
		target_date=datetime.strptime(filename_info[1],derby_elasticsearch_date_format).date()
		supplier_name=filename_info[0]
		return {'supplier_name':supplier_name,'target_date':target_date}
	pass