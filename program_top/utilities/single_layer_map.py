# -*- coding: utf-8 -*-
class single_layer_map(object):
	'''携带固定参数的map'''
	def do_work(self,each_iter_data):
		return self.__handling_function(self.__constant_parameter,each_iter_data)

	def __init__(self,handling_function,constant_parameter,iterable_data):
		super(single_layer_map, self).__init__()
		self.__constant_parameter=constant_parameter
		self.__handling_function=handling_function
		self.result=[self.__handling_function(each_iter)for each_iter in iterable_data]
		pass
	pass

class multilayer_map(object):
	'''
	只接受一个单组参数处理的函数(入参必须是列表)，一组固定参数，一组多维度迭代参数(必须是列表)
	'''
	def __init__(self,each_handling_function,constant_parameters,multi_dimension_iterable_data):
		super(multilayer_map, self).__init__()
		self.__constant_parameter=constant_parameters
		self.__handling_function=each_handling_function
		self.__variable_parameter=multi_dimension_iterable_data
		self.__max_indices=[len(each_iterable) for each_iterable in multi_dimension_iterable_data]
		min_indices=[0]*len(multi_dimension_iterable_data)
		self.__current_index=min_indices

		self.result=[]
		self.__yielder()
		pass

	def __yielder(self):
		while 1:
			current_changing_parameter=[self.__variable_parameter[each_deci][self.__current_index[each_deci]] for each_deci in xrange(0, len(self.__variable_parameter))]
			self.result.append(self.__handling_function(self.__constant_parameter, current_changing_parameter))

			if not self.__get_next_index(0):
				break
			pass

	def __get_next_index(self,n_th):
		if n_th==self.__max_indices.__len__():#如果当前指标已经大于末位，则迭代完成，结束运行时
			return None

		try_next=self.__current_index[n_th]+1
		current_deci_max=self.__max_indices[n_th]

		if try_next==current_deci_max:#如果当前位数指标已经达到最大，则当前指标重置为0，拨动下一位指标
			self.__current_index[n_th]=0
			return self.__get_next_index(n_th+1)
		else:#如果当前指标没有达到最大
			self.__current_index[n_th]+=1
			return self.__current_index
		pass
	pass





