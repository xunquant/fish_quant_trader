# encoding: UTF-8
import itertools
import os
import requests
from datetime import timedelta, datetime

from program_top.stdafx import my_path

from program_top.components.standalone_working_class.working_type_base import backend_interface_base
from program_top.utilities import my_datetime, my_dir

class s3_gate_uploader(backend_interface_base):
	'''
	递归的上传文件夹中的所有文件到s3_gate上，文件夹名称不变，但是每个文件在上面要给文件名留下日期时间戳，先传入/data_analysis/test根目录，如果OK再传入正式根目录
	'''

	def __init__(self):
		super(s3_gate_uploader, self).__init__()
		testing_root_path='testing_root'
		production_root_path='production_root'
		self._update_period=timedelta(days=int(self._business_config['repeating_days']))
		self._online_root=self._business_config['s3_gate_address']+self._business_config['target_stem_path']+production_root_path+'/'
		self._local_root=my_path.output_path
		self._inclusive_upload_mission_list=[]
		self._exclusive_upload_mission_list=[]
		self.__load_target_path_names('s3_uploading_path.csv')
		self._periodically_do(self._update_period,self.__do_upload_missions)
		#self.__do_upload_missions()
		pass

	def __do_upload_missions(self):
		[self._inclusive_upload_stem_path(each_stem_path)for each_stem_path in self._inclusive_upload_mission_list]
		pass

	def __upload_one_local_file_with_date_stamp(self, local_absolute_filename):
		'''
		将本地文件带上时间戳上传
		'''
		online_filename=self.__generate_online_inclusive_filename_according_to_local_absolute_name(local_absolute_filename)
		self.__write_ever_file_to_s3gate(online_filename,local_absolute_filename)
		pass

	def __generate_online_inclusive_filename_according_to_local_absolute_name(self,local_absolute_filename):
		'''
		根据线下版的全文件名生成线上的全文件名
		'''
		date_today=datetime.now().date()
		today_string=date_today.strftime(my_datetime.data_buffer_date_format)
		online_filename=local_absolute_filename.replace(self._local_root,self._online_root)
		new_online_fullname=online_filename.replace('.csv','_'+today_string+'.csv')
		new_online_fullname=new_online_fullname.replace(os.sep,'/')
		return new_online_fullname

	def _inclusive_upload_stem_path(self,source_stem_path,destination_path=None):
		'''
		把source_path/a/文件夹下的东西一起上传到root/destination/a/之下，如果没有a文件夹，s3gate会在云端创建
		'''
		for dir_name, sub_dir_list, file_list in os.walk(source_stem_path):
			[self.__upload_one_local_file_with_date_stamp(dir_name+each_file_name) for each_file_name in file_list]
			pass
		pass

	def __write_ever_file_to_s3gate(self,online_destination_filename,offline_source_absolute_filename):
		'''将线下文件写到线上'''
		file_open_2=open(offline_source_absolute_filename,mode='rb')
		test_response=requests.put(url=online_destination_filename, data=file_open_2)
		pass

	def _exclusive_upload_all_in_a_stem_path(self,source_stem_path,destination_path=None):
		'''
		把source_path/a/文件夹内的东西上传到root/destination/之下
		'''
		pass

	def __load_target_path_names(self,resource_path_list_filename):
		'''
		加载inclusive上传的文件夹列表
		'''
		absolute_filename=self._resource_directory+resource_path_list_filename
		target_classes_to_upload_output=self._load_multiline_csv(absolute_filename)
		upload_class_list=list(itertools.chain(*[each_dict.values() for each_dict in target_classes_to_upload_output]))
		current_mission_list=[my_dir.get_output_path_from_class_name(each_class_name) for each_class_name in upload_class_list]
		self._inclusive_upload_mission_list.extend(current_mission_list)
		pass
	pass