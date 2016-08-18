# -*- coding: utf-8 -*-

'''
和字符串相关的
'''

import re

to_string_if_unicode=lambda x:(x.encode('utf-8') if isinstance(x,unicode) else x)

def mapper_replace(original_string,mapper_dict):
	'''根据字典映射来更改原字符串里面的字符串，找到了字典里面的键就替换成字典里面的值，返回新字符串'''
	mapper_dict=mapper_dict
	text=original_string

	regex=re.compile('|'.join(map(re.escape, mapper_dict)))

	def one_xlat(match):
		return mapper_dict[match.group(0)]

	return regex.sub(one_xlat, text)
	pass