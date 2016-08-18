# encoding: UTF-8
import os
import re
from datetime import timedelta,datetime

from program_top.stdafx import my_path

from program_top.components.standalone_working_class.working_type_base import backend_interface_base
from program_top.components.standalone_working_class.working_type_base import curl_perflog_of_certain_type
from program_top.utilities import my_datetime
from program_top.utilities.my_dir import browse_dir

class buffer_cleaning_up(backend_interface_base):
	'''周期性定期删除文件，周期为配置文件中的repeating_day参数，原始数据缓存保留的天数为day_of_retension参数'''
	def __init__(self):
		super(buffer_cleaning_up, self).__init__()
		raw_data_instance_name=curl_perflog_of_certain_type.__name__
		self.raw_data_path=my_path.output_path+raw_data_instance_name+os.sep
		days_of_retention=int(self._business_config['day_of_retension'])
		date_today=datetime.now().date()
		self.oldest_retaining_day=date_today-timedelta(days=days_of_retention)#保留文件的最后日期
		repeating_day=int(self._business_config['repeating_day'])
		self._periodically_do(timedelta(days=repeating_day),self.__do_cleaning_up)
		pass

	def __do_cleaning_up(self):
		map(self.__delete_if_too_early_on_each_file,browse_dir(self.raw_data_path))
		log_string='周期性数据清理完毕'
		self._write_logs(log_string)
		pass

	def __delete_if_too_early_on_each_file(self,absolute_filename):
		relative_filename_list=absolute_filename.split(os.sep)
		relative_filename=relative_filename_list.pop()
		split_again=re.split('[._]',relative_filename)
		current_file_date=datetime.strptime(split_again[1],my_datetime.derby_elasticsearch_date_format)
		if current_file_date.date()<self.oldest_retaining_day:
			os.remove(absolute_filename)
		pass
	pass