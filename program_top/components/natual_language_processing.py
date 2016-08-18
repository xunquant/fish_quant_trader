# -*- coding: utf-8 -*-

'''
自然语言处理相关组件，主要是训练语法
'''

from nltk.tree import Tree
from program_top.components import component_base

class dictionary(component_base):
	'''字典类'''
	def __init__(self,binding_instance):
		super(dictionary, self).__init__(binding_instance)
		pass
	pass


def is_tree_end(tree_node):
	'''
	传入tree节点，返回自己是否已经是末端
	'''
	is_tree_self=isinstance(tree_node,Tree)#自己本身是否是tree节点
	length=tree_node.__len__()#本节点的子节点个数
	branch_is_not_tree=not isinstance(tree_node[0],Tree)#子节点不是tree

	return True if (is_tree_self and (length==1) and branch_is_not_tree) else False
	pass


def get_synsets(target_word,text_scope=None,caring_word_sets=None):
	'''

	:param target_word:要找寻同义词的目标词汇
	:type target_word:
	:param text_scope: 要找寻同义词的文章范围
	:type text_scope:
	:param caring_word_sets: 关注的同义词集合
	:type caring_word_sets:
	:return:
	:rtype:
	'''

	pass