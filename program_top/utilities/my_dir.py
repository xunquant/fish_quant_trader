# -*- coding: utf-8 -*-
import os,shutil

path_deshell=lambda absolute_path:(absolute_path[:-1])#文件夹路径脱壳，去掉末尾的os.sep字符

def make_ever_dir(raw_path):
	'''
	无论如何创建这个文件夹
	'''
	target_path=raw_path
	is_existing=os.path.exists(target_path)
	if not is_existing:
		os.makedirs(target_path)
	pass

def del_file_ever(target_file):
	'''
	删除目标文件，如果存在就删除
	'''
	if os.path.isfile(target_file):
		os.remove(target_file)

def browse_dir(absolute_path,appendix=None):
	'''
	遍历文件夹主干下的所有子文件夹和文件
	'''
	current_layer_files=[]

	appendix_determine=(lambda x: (isinstance(x,str) and x.endswith(appendix))) if appendix else None

	for dir_name,sub_dir_list,file_list in os.walk(absolute_path):
		absolute_file_list=[dir_name+os.sep+each_file_name for each_file_name in filter(appendix_determine,file_list)]
		current_layer_files.extend(absolute_file_list)
		pass
	return current_layer_files

def clear_dir_tree(absolute_path):
	'''
	清理文件夹树以下的文件，但不删除文件本身
	'''
	for dir_name,sub_dir_list,file_list in os.walk(absolute_path):
		[os.remove(dir_name+os.sep+each_file_name) for each_file_name in file_list]#清除本层下所有文件
		[shutil.rmtree(dir_name+os.sep+each_dir) for each_dir in sub_dir_list]#清除本层下所有子文件夹
		pass
	pass

def get_relative_filename_from_absolute(absolute_filename):
	filename_list=absolute_filename.split(os.sep)
	return filename_list.pop()