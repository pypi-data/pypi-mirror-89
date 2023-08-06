from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HetbInfo:
	"""HetbInfo commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hetbInfo", core, parent)

	# noinspection PyTypeChecker
	class UphInfoStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Burst_Power: float: float Indication of HE TB burst power. Range: -999 dBm to 999 dBm
			- Uph: int: decimal Indication of UL power headroom. Range: 0 dB to 31 dB
			- Min_Tx_Power_Flag: bool: OFF | ON Indication whether the HE TB bursts are sent at the minimum transmit power of the station."""
		__meta_args_list = [
			ArgStruct.scalar_float('Burst_Power'),
			ArgStruct.scalar_int('Uph'),
			ArgStruct.scalar_bool('Min_Tx_Power_Flag')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Burst_Power: float = None
			self.Uph: int = None
			self.Min_Tx_Power_Flag: bool = None

	def get_uph_info(self) -> UphInfoStruct:
		"""SCPI: SENSe:WLAN:SIGNaling<instance>:HETBinfo:UPHinfo \n
		Snippet: value: UphInfoStruct = driver.sense.hetbInfo.get_uph_info() \n
		Queries actual information related to uplink power headroom (UPH) control. \n
			:return: structure: for return value, see the help for UphInfoStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:WLAN:SIGNaling<Instance>:HETBinfo:UPHinfo?', self.__class__.UphInfoStruct())
