# -*- coding: utf-8 -*-

import datetime,logging,time

class my_logging_format(logging.Formatter):#我的日志时间格式，包含毫秒
	def formatTime(self, record, datefmt=None):

		ct=self.converter(record.created)
		if datefmt:
			s=time.strftime(datefmt,ct)
		else:
			s=str(datetime.datetime.now())
			pass
		return s
	pass

logger_name='my_log'

the_logger=logging.getLogger(logger_name)
the_logger.setLevel(logging.CRITICAL)
the_log_format=logging.Formatter()
from program_top.stdafx.my_path import log_path
log_filename=log_path+logger_name+'.txt'
log_file=logging.FileHandler(log_filename)
log_file.setLevel(logging.CRITICAL)
log_file.setFormatter(the_log_format)
the_logger.addHandler(log_file)

log_print=logging.StreamHandler()
log_print.setLevel(logging.CRITICAL)
log_print.setFormatter(the_log_format)
the_logger.addHandler(log_print)

