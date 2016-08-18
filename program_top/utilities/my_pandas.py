# encoding: UTF-8

def dataframe_element_wise_prepare(dataframe_data,data_content_key):
	'''
	实质上是将 data_content_key字段作为数值，其他指标都作为index做多分组，然后各组求和，返回的dataframe携带多指标参数
	'''
	test=dataframe_data._series.keys()
	test.remove(data_content_key)
	return dataframe_data.groupby(test).sum()

def dataframe_index_back_to_key(dataframe_with_index):
	'''
	把有index的数据dataframe还原入数据字段
	'''
	current_multi_index=dataframe_with_index.index


	for each_index in current_multi_index.names:
		dataframe_with_index[each_index]=current_multi_index.get_level_values(each_index)
		pass
	'''
	for each_column in current_multi_column.names:
		dataframe_with_index[each_column]=current_multi_column.get_level_values(each_column)
		pass
	'''
	return dataframe_with_index.reset_index(drop=True)

def dataframe_value_filter(target_dataframe, target_series_name, transform_func):
	'''
	针对target_dataframe的target_series_name序列(无index，只有字段)，使用transform_func函数做映射，转换完成以后返回新的dataframe
	'''
	changing_series=target_dataframe[target_series_name]
	new_series=changing_series.apply(transform_func)
	target_dataframe[target_series_name]=new_series
	return target_dataframe