# -*- coding: utf-8 -*-

from program_top.utilities.string_and_unicode import mapper_replace

def covering_merge_dicts(list_of_dicts_to_merge):
	'''覆盖性的合并所有dict，后来写入的值覆盖之前写入的值'''
	empty_dict={}

	for each_dict in list_of_dicts_to_merge:
		empty_dict.update(each_dict)
		pass

	return empty_dict

def union_merge_dict(list_of_dicts_to_merge):
	'''保守联合型的合并字典，如果某一个键上两个字典都有值，则合并为一个list'''

	new_dict={}

	for each_dict in list_of_dicts_to_merge:
		for each_key in each_dict.keys():
			if new_dict.has_key(each_key):#如果现有dict已经有了这个key
				new_dict[each_key]=list_safe_merge(new_dict[each_key],each_dict[each_key],overlap_identical=True)
			else:#如果现有的字典没有这个key
				new_dict[each_key]=each_dict[each_key]
				pass
			pass
		pass

	return new_dict
	pass

def list_safe_extend(original_list,coming_obj):
	'''安全延展list，如果纳入的对象是个list就延展，否则就插入，如果输入的对象为空，就不改动输出原来的对象'''
	if not coming_obj:
		return original_list

	if isinstance(coming_obj, list):
		original_list.extend(coming_obj)
	else:
		original_list.append(coming_obj)

	return original_list

def list_safe_merge(list_obj_a,list_obj_b,overlap_identical=True):
	'''安全合并两个元素，返回合并以后的List，选择当两个元素相等的时候是否重叠'''
	new_list=[]
	new_list=list_safe_extend(new_list,list_obj_a)

	if (not overlap_identical) or (list_obj_a!=list_obj_b):#如果a和b元素不相等，或者函数调用不介意两个元素相等，才把b也汇入进去——换句话说
		new_list=list_safe_extend(new_list,list_obj_b)

	return new_list

def give_options_get_choices(options_list):
	'''展示str列表，作为选项，读取用户的选择，并根据选择生成新的字符串'''
	current_list=[]
	option_mapper={}

	for each_index in xrange(options_list.__len__()):
		current_option=(each_index,options_list[each_index])
		current_list.append(current_option)
		option_dict={str(each_index):options_list[each_index]}
		option_mapper.update(option_dict)
		pass

	user_option_string=raw_input(current_list.__repr__())
	replaced_string=mapper_replace(user_option_string,option_mapper)
	return replaced_string

def get_levels_list_in_dict(list_as_new_level_dict_keys):
	'''使用一个list作为新字典的逐个key，每个key后面带一个空列表'''
	out_dict=dict([(each_key,[]) for each_key in list_as_new_level_dict_keys])
	return out_dict
