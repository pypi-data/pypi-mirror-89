from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Qos:
	"""Qos commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("qos", core, parent)

	# noinspection PyTypeChecker
	def get_etoe(self) -> enums.Tid:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:QOS:ETOE \n
		Snippet: value: enums.Tid = driver.configure.connection.qos.get_etoe() \n
		Sets the TID value to be used for the end-to-end connection using DAU. \n
			:return: tid: TID0 | TID1 | TID2 | TID3 | TID4 | TID5 | TID6 | TID7
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:QOS:ETOE?')
		return Conversions.str_to_scalar_enum(response, enums.Tid)

	def set_etoe(self, tid: enums.Tid) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:QOS:ETOE \n
		Snippet: driver.configure.connection.qos.set_etoe(tid = enums.Tid.TID0) \n
		Sets the TID value to be used for the end-to-end connection using DAU. \n
			:param tid: TID0 | TID1 | TID2 | TID3 | TID4 | TID5 | TID6 | TID7
		"""
		param = Conversions.enum_scalar_to_str(tid, enums.Tid)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:QOS:ETOE {param}')

	# noinspection PyTypeChecker
	def get_prioritiz(self) -> enums.PrioMode:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:QOS:PRIoritiz \n
		Snippet: value: enums.PrioMode = driver.configure.connection.qos.get_prioritiz() \n
			INTRO_CMD_HELP: Prioritization mode selects the transmission sequence. \n
			- Round-robin schedules equal transmission time to each TID
			- TID priority selection prioritizes the transmission of highest TID values \n
			:return: mode: ROURobin | TIDPriority
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:QOS:PRIoritiz?')
		return Conversions.str_to_scalar_enum(response, enums.PrioMode)

	def set_prioritiz(self, mode: enums.PrioMode) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:QOS:PRIoritiz \n
		Snippet: driver.configure.connection.qos.set_prioritiz(mode = enums.PrioMode.ROURobin) \n
			INTRO_CMD_HELP: Prioritization mode selects the transmission sequence. \n
			- Round-robin schedules equal transmission time to each TID
			- TID priority selection prioritizes the transmission of highest TID values \n
			:param mode: ROURobin | TIDPriority
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.PrioMode)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:QOS:PRIoritiz {param}')

	# noinspection PyTypeChecker
	def get_bar_method(self) -> enums.BarMethod:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:QOS:BARMethod \n
		Snippet: value: enums.BarMethod = driver.configure.connection.qos.get_bar_method() \n
		Specifies the method used to request a BlockAck frame from the DUT \n
			:return: method: IMPBar | EXPBar | MUBar Implicit, explicit or multi-user block acknowledgment request
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:QOS:BARMethod?')
		return Conversions.str_to_scalar_enum(response, enums.BarMethod)

	def set_bar_method(self, method: enums.BarMethod) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:QOS:BARMethod \n
		Snippet: driver.configure.connection.qos.set_bar_method(method = enums.BarMethod.EXPBar) \n
		Specifies the method used to request a BlockAck frame from the DUT \n
			:param method: IMPBar | EXPBar | MUBar Implicit, explicit or multi-user block acknowledgment request
		"""
		param = Conversions.enum_scalar_to_str(method, enums.BarMethod)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:QOS:BARMethod {param}')

	# noinspection PyTypeChecker
	class BlackStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Tid_0: bool: No parameter help available
			- Tid_1: bool: No parameter help available
			- Tid_2: bool: No parameter help available
			- Tid_3: bool: No parameter help available
			- Tid_4: bool: No parameter help available
			- Tid_5: bool: No parameter help available
			- Tid_6: bool: No parameter help available
			- Tid_7: bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Tid_0'),
			ArgStruct.scalar_bool('Tid_1'),
			ArgStruct.scalar_bool('Tid_2'),
			ArgStruct.scalar_bool('Tid_3'),
			ArgStruct.scalar_bool('Tid_4'),
			ArgStruct.scalar_bool('Tid_5'),
			ArgStruct.scalar_bool('Tid_6'),
			ArgStruct.scalar_bool('Tid_7')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Tid_0: bool = None
			self.Tid_1: bool = None
			self.Tid_2: bool = None
			self.Tid_3: bool = None
			self.Tid_4: bool = None
			self.Tid_5: bool = None
			self.Tid_6: bool = None
			self.Tid_7: bool = None

	def get_black(self) -> BlackStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:QOS:BLACk \n
		Snippet: value: BlackStruct = driver.configure.connection.qos.get_black() \n
		Enables/ disables a block ack session per TID (8 values) . \n
			:return: structure: for return value, see the help for BlackStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:QOS:BLACk?', self.__class__.BlackStruct())

	def set_black(self, value: BlackStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:QOS:BLACk \n
		Snippet: driver.configure.connection.qos.set_black(value = BlackStruct()) \n
		Enables/ disables a block ack session per TID (8 values) . \n
			:param value: see the help for BlackStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:QOS:BLACk', value)
