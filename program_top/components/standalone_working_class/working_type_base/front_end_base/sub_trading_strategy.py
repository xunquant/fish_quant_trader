# encoding: UTF-8

from datetime import datetime

from program_top.components.standalone_working_class.working_type_base import front_end_base
from program_top.utilities import my_datetime

class sub_trading_strategy(front_end_base):
	'''
	子策略基类
	'''
	def __init__(self,hub_strategy_ref=None,strategy_config=None):
		'''
		初始化任务：
		1.加载品种信息
		2.读取对应品种的数据序列或面板
		3.加载当前的账号信息情况，确定目前的持仓、订单，本策略可以使用的资金配额(每一笔订单要有所属策略的标签，成交以后，留在主账户中的对应持仓记录必须注明是哪个策略产生的)
		4.一个子策略只对应一个账户当中的一个交易品种

		具体策略的初始化任务：
		1.加载策略函数和若干个事件的处理函数(策略逻辑本身)
		'''
		super(sub_trading_strategy, self).__init__()
		self.strategy_name=strategy_config['sub_strategy_name']
		self.weight_percentatge=float(strategy_config['max_weight'])
		self._data_period=my_datetime.get_timedelta_from_string(strategy_config['period'])#数据周期
		self._is_backtesting=(strategy_config['backtest_or_trading']=='backtest')#是否是策略回验，如果是实盘或者模拟盘那就是trading，否则为backtest

		if self._is_backtesting:
			self._backtest_start=datetime.strptime(strategy_config['start_moment_if_backtest'],my_datetime.data_buffer_date_format)
			self._backtest_end=datetime.strptime(strategy_config['end_moment_if_backtest'],my_datetime.data_buffer_date_format)

		pass

	def _data_panel_initialisation(self, date_back_time=None):
		'''
		某个品种从指定时刻开始的回溯数据面板初始化，具体继承
		'''
		pass
	pass