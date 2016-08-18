# -*- coding: utf-8 -*-
import datetime,time

my_date_time_microsec_format='%Y-%m-%d-%H:%M:%S.%f'#年月日时分秒微秒
my_date_time_without_micro='%Y-%m-%d-%H:%M:%S'#年月日时分秒微秒
my_quant_time_format='%Y-%m-%d %H:%M:%S'#掘金时间格式yyyy-mm-dd HH:MM:SS
my_quant_time_stamp_format='%Y-%m-%dT%H:%M:%S+08:00'#掘金时间戳格式
data_buffer_time_format='%Y-%m-%d-%H-%M-%S.%f'#数据缓存文件时间格式yyyy-mm-dd-HH-MM-SS.μs
data_buffer_date_format='%Y-%m-%d'#数据缓存文件日期格式yyyy-mm-dd
date_contract_format='%Y%m'
trading_day_closing_prepare_time=datetime.time(14,59,50)
trading_day_closing_complete_time=datetime.time(20,00,00)
derby_elasticsearch_date_format='%Y%m%d'#elasticsearch日期格式
derby_perflog_timestamp_format='%Y-%m-%d-%H:%M:%S.%f-%Z'#年月日时分秒

def utc_float2datetime(utc_float_time):
	int_utc_sec=int(utc_float_time)
	millisec_float=int(1000*(utc_float_time-int_utc_sec))
	time_t=time.localtime(int_utc_sec)
	final_datetime=datetime.datetime(time_t.tm_year,time_t.tm_mon,time_t.tm_mday,time_t.tm_hour,time_t.tm_min,time_t.tm_sec,millisec_float*1000)
	return final_datetime
	pass

def my_date_time_string2datetime(time_string):
	return datetime.datetime.strptime(time_string, my_date_time_without_micro)

#返回月首日期
def get_month_1st_date(target_date=datetime.datetime.today().date()):
	return datetime.date(target_date.year,target_date.month,1)

#返回n年后的同一天
def get_same_day_in_next_n_year(target_date=datetime.datetime.today().date(),n=1):
	if target_date.month==2 and target_date.day==29:
		return datetime.date(target_date.year+n,2,28)#如果输入日期是2月29日，则返回n年后的2月28日
	return datetime.date(target_date.year+n,target_date.month,target_date.day)
#返回n月后的同一天

def get_same_day_in_next_n_month(target_date=datetime.datetime.today().date(),n=1):
	new_month=target_date.month+1
	new_year=target_date.year
	if new_month>12:#如果大于12了，则进位
		new_month=1
		new_year+=1
	if n>1:#如果n为1，返回下个月本日
		return get_same_day_in_next_n_month(datetime.date(new_year,new_month,1),n-1)
	else:
		return datetime.date(new_year,new_month,1)

