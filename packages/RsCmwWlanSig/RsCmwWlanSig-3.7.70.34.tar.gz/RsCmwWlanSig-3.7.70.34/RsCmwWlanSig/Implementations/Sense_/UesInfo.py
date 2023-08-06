from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UesInfo:
	"""UesInfo commands group definition. 6 total commands, 3 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("uesInfo", core, parent)

	@property
	def antenna(self):
		"""antenna commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_antenna'):
			from .UesInfo_.Antenna import Antenna
			self._antenna = Antenna(self._core, self._base)
		return self._antenna

	@property
	def ueAddress(self):
		"""ueAddress commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ueAddress'):
			from .UesInfo_.UeAddress import UeAddress
			self._ueAddress = UeAddress(self._core, self._base)
		return self._ueAddress

	@property
	def cmwAddress(self):
		"""cmwAddress commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cmwAddress'):
			from .UesInfo_.CmwAddress import CmwAddress
			self._cmwAddress = CmwAddress(self._core, self._base)
		return self._cmwAddress

	def get_rxb_power(self) -> float:
		"""SCPI: SENSe:WLAN:SIGNaling<instance>:UESinfo:RXBPower \n
		Snippet: value: float = driver.sense.uesInfo.get_rxb_power() \n
		Queries the average power of the last burst received from the DUT. \n
			:return: power: float Unit: dBm
		"""
		response = self._core.io.query_str('SENSe:WLAN:SIGNaling<Instance>:UESinfo:RXBPower?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	class DrateStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Format_Py: enums.FrameFormat: NHT | HT | VHT | HE Frame format NHT: non-high throughput format (non-HT) HT: high throughput format VHT: very high throughput format HE: high efficiency format
			- Rate: enums.DataRate: MB1 | MB2 | MB5 | MB6 | MB9 | MB11 | MB12 | MB18 | MB24 | MB36 | MB48 | MB54 | MCS0 | MCS1 | MCS2 | MCS3 | MCS4 | MCS5 | MCS6 | MCS7 | MCS8 | MCS9 | MCS10 | MCS11 | MCS12 | MCS13 | MCS14 | MCS15 MBx: data rate for NHT in Mbit/s {1, 2, 5.5, 6, 9, 11, 12, 18, 24, 36, 48, 54} MCSx: modulation and coding scheme x for HT, VHT and HE
			- Cbw: enums.ChannelBandwidth: BW20 | BW40 | BW80 | BW88 | BW16 Channel bandwidth in MHz: 20, 40, 80, 80+80, 160
			- Nss: enums.SpacialStreamsNr: NSS1 | NSS2 | NSS3 | NSS4 | NSS5 | NSS6 | NSS7 | NSS8 Number of spatial streams"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Format_Py', enums.FrameFormat),
			ArgStruct.scalar_enum('Rate', enums.DataRate),
			ArgStruct.scalar_enum('Cbw', enums.ChannelBandwidth),
			ArgStruct.scalar_enum('Nss', enums.SpacialStreamsNr)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Format_Py: enums.FrameFormat = None
			self.Rate: enums.DataRate = None
			self.Cbw: enums.ChannelBandwidth = None
			self.Nss: enums.SpacialStreamsNr = None

	# noinspection PyTypeChecker
	def get_drate(self) -> DrateStruct:
		"""SCPI: SENSe:WLAN:SIGNaling<instance>:UESinfo:DRATe \n
		Snippet: value: DrateStruct = driver.sense.uesInfo.get_drate() \n
		Queries information related to the data rate of the DUT signal. \n
			:return: structure: for return value, see the help for DrateStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:WLAN:SIGNaling<Instance>:UESinfo:DRATe?', self.__class__.DrateStruct())

	# noinspection PyTypeChecker
	class AbsReportStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Total: int: decimal Maximum of all reports received in preceding interval Range: 0 bits to 4.145152E+6 bits
			- Buffered_Data_Tid: int: decimal Maximum of all QoS control reports Range: 0 bits to 4.145152E+6 bits
			- Tidx: enums.Tid: TID0 | TID1 | TID2 | TID3 | TID4 | TID5 | TID6 | TID7 Indication of TID, for which the buffer status BufferedData_TID is reported
			- Buffered_Data_Ac: int: decimal Maximum AC-specific queue size of all AC control reports Range: 0 bits to 4.145152E+6 bits
			- Acx: enums.AccessCategory: ACBE | ACBK | ACVI | ACVO Indication of access category (ACI bitmap subfield) for which the buffer status BufferedData_AC is reported ACBE: AC_BE (best effort) ACBK: AC_BK (background) ACVI: AC_VI (video) ACVO: AC_VO (voice)"""
		__meta_args_list = [
			ArgStruct.scalar_int('Total'),
			ArgStruct.scalar_int('Buffered_Data_Tid'),
			ArgStruct.scalar_enum('Tidx', enums.Tid),
			ArgStruct.scalar_int('Buffered_Data_Ac'),
			ArgStruct.scalar_enum('Acx', enums.AccessCategory)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Total: int = None
			self.Buffered_Data_Tid: int = None
			self.Tidx: enums.Tid = None
			self.Buffered_Data_Ac: int = None
			self.Acx: enums.AccessCategory = None

	def get_abs_report(self) -> AbsReportStruct:
		"""SCPI: SENSe:WLAN:SIGNaling<instance>:UESinfo:ABSReport \n
		Snippet: value: AbsReportStruct = driver.sense.uesInfo.get_abs_report() \n
		Indicates reported buffered data for a UE supporting a HE buffer status report (BSR) control field. \n
			:return: structure: for return value, see the help for AbsReportStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:WLAN:SIGNaling<Instance>:UESinfo:ABSReport?', self.__class__.AbsReportStruct())

	def clone(self) -> 'UesInfo':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UesInfo(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
