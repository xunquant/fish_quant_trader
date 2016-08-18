# -*- coding: utf-8 -*-

from csv import DictWriter,excel

class by_row_dialect(excel):
	def __init__(self):
		self.delimiter=self.lineterminator

class pure_empty_class:#纯空类，如果传入字典参数，则使用字典来给各成员初始化
	def __init__(self, incoming_dict=None):
		if incoming_dict is not None:
			self.__dict__.update(incoming_dict)
			pass
		pass

#在指定的文件打印本实例所有成员
	def print_all(self, print_filename=None):
		if print_filename:
			csv_file=open(print_filename,mode='w')
			current_dict=self.__dict__
			all_keys=current_dict.keys()
			the_writer=DictWriter(csv_file,all_keys)
			the_writer.writerow(current_dict)
			csv_file.close()
			pass
		pass
	pass