# -*- coding: utf-8 -*-

import requests,json

def download_get(online_file_url, local_buffering_absolute_filename=None):
	'''
	如果指定存储路径则写入to do
	如果没有指定则直接返回读到的结果
	'''
	loaded_content=None

	try:#尝试读取缓存文件
		with open(local_buffering_absolute_filename) as filestruct:
			loaded_content=json.loads(filestruct.read())
			pass
	except:#如果没有缓存文件
		try:#尝试下载
			print('no cache, now about to download:%s'%(online_file_url))
			response=requests.get(online_file_url)
			loaded_content=json.loads(response.content)
		except:
			print '下载失败，注意检查'
			return None

		try:#如果到此下载完成，但还没有保存，则尝试保存
			with open(local_buffering_absolute_filename,mode='w') as filestruct_write:
				filestruct_write.write(json.dumps(loaded_content))
				pass
		except:
			pass

		pass

	return loaded_content
	pass

def curl_a_post(post_url, query_target_dict):
	'''
	:param post_url:发出连接的url
	:type post_url: 字符串
	:param query_target_dict:查询目标数据类别
	:type query_target_dict: 字典
	:return: 返回结果
	:rtype:
	'''
	query_json_string=json.dumps(query_target_dict)
	response=requests.post(post_url, data=query_json_string)
	results=json.loads(response.text)
	return results

def is_url_existing(target_url):
	'''
	判断一个url是否存在内容
	'''

	response=requests.get(target_url)
	if response.status_code==200:
		return True
	else:
		return False

	pass