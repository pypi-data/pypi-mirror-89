from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hetf:
	"""Hetf commands group definition. 20 total commands, 1 Sub-groups, 19 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hetf", core, parent)

	@property
	def ssTx(self):
		"""ssTx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssTx'):
			from .Hetf_.SsTx import SsTx
			self._ssTx = SsTx(self._core, self._base)
		return self._ssTx

	def get_txp(self) -> int:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:TXP \n
		Snippet: value: int = driver.configure.connection.hetf.get_txp() \n
		Sets the interval for periodical trigger frame. \n
			:return: interval: integer Range: 1 to 10E+3, Unit: ms
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:TXP?')
		return Conversions.str_to_int(response)

	def set_txp(self, interval: int) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:TXP \n
		Snippet: driver.configure.connection.hetf.set_txp(interval = 1) \n
		Sets the interval for periodical trigger frame. \n
			:param interval: integer Range: 1 to 10E+3, Unit: ms
		"""
		param = Conversions.decimal_value_to_str(interval)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:TXP {param}')

	def get_txen(self) -> bool:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:TXEN \n
		Snippet: value: bool = driver.configure.connection.hetf.get_txen() \n
		Enables/ disables the periodical trigger frame. \n
			:return: state: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:TXEN?')
		return Conversions.str_to_bool(response)

	def set_txen(self, state: bool) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:TXEN \n
		Snippet: driver.configure.connection.hetf.set_txen(state = False) \n
		Enables/ disables the periodical trigger frame. \n
			:param state: OFF | ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:TXEN {param}')

	def get_nss(self) -> int:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:NSS \n
		Snippet: value: int = driver.configure.connection.hetf.get_nss() \n
		Queries the number of HE TB PPDU spatial streams. \n
			:return: number_ss: decimal Range: 1 to 8
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:NSS?')
		return Conversions.str_to_int(response)

	def get_sss(self) -> int:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:SSS \n
		Snippet: value: int = driver.configure.connection.hetf.get_sss() \n
		Queries the starting spatial stream for the HE TB PPDU. \n
			:return: starting_ss: decimal Range: 1 to 8
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:SSS?')
		return Conversions.str_to_int(response)

	def get_dcm(self) -> bool:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:DCM \n
		Snippet: value: bool = driver.configure.connection.hetf.get_dcm() \n
		Specifies whether the HE TB response uses dual carrier modulation (DCM) . \n
			:return: dc_m: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:DCM?')
		return Conversions.str_to_bool(response)

	def set_dcm(self, dc_m: bool) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:DCM \n
		Snippet: driver.configure.connection.hetf.set_dcm(dc_m = False) \n
		Specifies whether the HE TB response uses dual carrier modulation (DCM) . \n
			:param dc_m: OFF | ON
		"""
		param = Conversions.bool_to_str(dc_m)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:DCM {param}')

	# noinspection PyTypeChecker
	def get_mcs(self) -> enums.McsIndex:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:MCS \n
		Snippet: value: enums.McsIndex = driver.configure.connection.hetf.get_mcs() \n
		Specifies the modulation and coding scheme (MCS) used by the HE TB PPDU. \n
			:return: mcs: MCS | MCS1 | MCS2 | MCS3 | MCS4 | MCS5 | MCS6 | MCS7 | MCS8 | MCS9 | MCS10 | MCS11 MCS, MCS1,...,MCS11: MCS 0 to MCS 11
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:MCS?')
		return Conversions.str_to_scalar_enum(response, enums.McsIndex)

	def set_mcs(self, mcs: enums.McsIndex) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:MCS \n
		Snippet: driver.configure.connection.hetf.set_mcs(mcs = enums.McsIndex.MCS) \n
		Specifies the modulation and coding scheme (MCS) used by the HE TB PPDU. \n
			:param mcs: MCS | MCS1 | MCS2 | MCS3 | MCS4 | MCS5 | MCS6 | MCS7 | MCS8 | MCS9 | MCS10 | MCS11 MCS, MCS1,...,MCS11: MCS 0 to MCS 11
		"""
		param = Conversions.enum_scalar_to_str(mcs, enums.McsIndex)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:MCS {param}')

	# noinspection PyTypeChecker
	def get_ctyp(self) -> enums.CodingType:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:CTYP \n
		Snippet: value: enums.CodingType = driver.configure.connection.hetf.get_ctyp() \n
		Specifies the coding used by the HE TB PPDU. \n
			:return: type_py: BCC | LDPC
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:CTYP?')
		return Conversions.str_to_scalar_enum(response, enums.CodingType)

	def set_ctyp(self, type_py: enums.CodingType) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:CTYP \n
		Snippet: driver.configure.connection.hetf.set_ctyp(type_py = enums.CodingType.BCC) \n
		Specifies the coding used by the HE TB PPDU. \n
			:param type_py: BCC | LDPC
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.CodingType)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:CTYP {param}')

	# noinspection PyTypeChecker
	def get_rual(self) -> enums.RuAllocation:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:RUAL \n
		Snippet: value: enums.RuAllocation = driver.configure.connection.hetf.get_rual() \n
		Specifies the RU used by the HE TB PPDU. Refer to IEEE P802.11ax/D4.3, table 9-31h B7–B1 of the RU Allocation subfield. \n
			:return: ru_allocation: RU0 | RU1 | RU2 | RU3 | RU4 | RU5 | RU6 | RU7 | RU8 | RU9 | RU10 | RU11 | RU12 | RU13 | RU14 | RU15 | RU16 | RU17 | RU18 | RU19 | RU20 | RU21 | RU22 | RU23 | RU24 | RU25 | RU26 | RU27 | RU28 | RU29 | RU30 | RU31 | RU32 | RU33 | RU34 | RU35 | RU36 | RU37 | RU38 | RU39 | RU40 | RU41 | RU42 | RU43 | RU44 | RU45 | RU46 | RU47 | RU48 | RU49 | RU50 | RU51 | RU52 | RU53 | RU54 | RU55 | RU56 | RU57 | RU58 | RU59 | RU60 | RU61 | RU62 | RU63 | RU64 | RU65 | RU66 | RU67 | RU68 Bits 7 to 1 of the RU allocation subfield, see table below.
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:RUAL?')
		return Conversions.str_to_scalar_enum(response, enums.RuAllocation)

	def set_rual(self, ru_allocation: enums.RuAllocation) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:RUAL \n
		Snippet: driver.configure.connection.hetf.set_rual(ru_allocation = enums.RuAllocation.RU0) \n
		Specifies the RU used by the HE TB PPDU. Refer to IEEE P802.11ax/D4.3, table 9-31h B7–B1 of the RU Allocation subfield. \n
			:param ru_allocation: RU0 | RU1 | RU2 | RU3 | RU4 | RU5 | RU6 | RU7 | RU8 | RU9 | RU10 | RU11 | RU12 | RU13 | RU14 | RU15 | RU16 | RU17 | RU18 | RU19 | RU20 | RU21 | RU22 | RU23 | RU24 | RU25 | RU26 | RU27 | RU28 | RU29 | RU30 | RU31 | RU32 | RU33 | RU34 | RU35 | RU36 | RU37 | RU38 | RU39 | RU40 | RU41 | RU42 | RU43 | RU44 | RU45 | RU46 | RU47 | RU48 | RU49 | RU50 | RU51 | RU52 | RU53 | RU54 | RU55 | RU56 | RU57 | RU58 | RU59 | RU60 | RU61 | RU62 | RU63 | RU64 | RU65 | RU66 | RU67 | RU68 Bits 7 to 1 of the RU allocation subfield, see table below.
		"""
		param = Conversions.enum_scalar_to_str(ru_allocation, enums.RuAllocation)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:RUAL {param}')

	def get_ldpc(self) -> bool:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:LDPC \n
		Snippet: value: bool = driver.configure.connection.hetf.get_ldpc() \n
		Specifies the support of LDPC extra symbol segment. \n
			:return: extra_symbol: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:LDPC?')
		return Conversions.str_to_bool(response)

	def set_ldpc(self, extra_symbol: bool) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:LDPC \n
		Snippet: driver.configure.connection.hetf.set_ldpc(extra_symbol = False) \n
		Specifies the support of LDPC extra symbol segment. \n
			:param extra_symbol: OFF | ON
		"""
		param = Conversions.bool_to_str(extra_symbol)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:LDPC {param}')

	# noinspection PyTypeChecker
	class ApTxPowerStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Int_Value: int: decimal Range: 0 to 60
			- Dbm_Value: int: decimal Range: -20 dBm to 40 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Int_Value'),
			ArgStruct.scalar_int('Dbm_Value')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Int_Value: int = None
			self.Dbm_Value: int = None

	def get_ap_tx_power(self) -> ApTxPowerStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:APTXpower \n
		Snippet: value: ApTxPowerStruct = driver.configure.connection.hetf.get_ap_tx_power() \n
		Specifies the value of 'AP TX Power' the R&S CMW signals via a trigger frame. \n
			:return: structure: for return value, see the help for ApTxPowerStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:APTXpower?', self.__class__.ApTxPowerStruct())

	# noinspection PyTypeChecker
	def get_mltf(self) -> enums.MuMimoLongTrainField:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:MLTF \n
		Snippet: value: enums.MuMimoLongTrainField = driver.configure.connection.hetf.get_mltf() \n
		Sets MU-MIMO long training fields (LTF) . \n
			:return: mu_mimo_ltf: SING | MASK SING: single stream pilots MASK: mask LTF sequence of each spatial stream by a distinct orthogonal code
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:MLTF?')
		return Conversions.str_to_scalar_enum(response, enums.MuMimoLongTrainField)

	def set_mltf(self, mu_mimo_ltf: enums.MuMimoLongTrainField) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:MLTF \n
		Snippet: driver.configure.connection.hetf.set_mltf(mu_mimo_ltf = enums.MuMimoLongTrainField.MASK) \n
		Sets MU-MIMO long training fields (LTF) . \n
			:param mu_mimo_ltf: SING | MASK SING: single stream pilots MASK: mask LTF sequence of each spatial stream by a distinct orthogonal code
		"""
		param = Conversions.enum_scalar_to_str(mu_mimo_ltf, enums.MuMimoLongTrainField)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:MLTF {param}')

	# noinspection PyTypeChecker
	def get_gilt(self) -> enums.Giltf:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:GILT \n
		Snippet: value: enums.Giltf = driver.configure.connection.hetf.get_gilt() \n
		Specifies the guard interval and LTF type of the HE TB PPDU. Note, that according to standard IEEE 802.11ax draft 3.
		0, the value '1x LTF + 1.6 µs GI' is not supported for HE TB PPDU. \n
			:return: gi_ltf: L116 | L216 | L432 LTF type and corresponding GI: L116: 1x LTF + 1.6 µs GI L216: 2x LTF + 1.6 µs GI L432: 4x LTF + 3.2 µs GI
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:GILT?')
		return Conversions.str_to_scalar_enum(response, enums.Giltf)

	def set_gilt(self, gi_ltf: enums.Giltf) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:GILT \n
		Snippet: driver.configure.connection.hetf.set_gilt(gi_ltf = enums.Giltf.L116) \n
		Specifies the guard interval and LTF type of the HE TB PPDU. Note, that according to standard IEEE 802.11ax draft 3.
		0, the value '1x LTF + 1.6 µs GI' is not supported for HE TB PPDU. \n
			:param gi_ltf: L116 | L216 | L432 LTF type and corresponding GI: L116: 1x LTF + 1.6 µs GI L216: 2x LTF + 1.6 µs GI L432: 4x LTF + 3.2 µs GI
		"""
		param = Conversions.enum_scalar_to_str(gi_ltf, enums.Giltf)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:GILT {param}')

	# noinspection PyTypeChecker
	def get_chbw(self) -> enums.ChannelBandwidthDut:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:CHBW \n
		Snippet: value: enums.ChannelBandwidthDut = driver.configure.connection.hetf.get_chbw() \n
		Specifies the channel bandwidth of the HE TB PPDU. \n
			:return: bandwidth: BW20 | BW40 | BW80 | BW160
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:CHBW?')
		return Conversions.str_to_scalar_enum(response, enums.ChannelBandwidthDut)

	def set_chbw(self, bandwidth: enums.ChannelBandwidthDut) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:CHBW \n
		Snippet: driver.configure.connection.hetf.set_chbw(bandwidth = enums.ChannelBandwidthDut.BW160) \n
		Specifies the channel bandwidth of the HE TB PPDU. \n
			:param bandwidth: BW20 | BW40 | BW80 | BW160
		"""
		param = Conversions.enum_scalar_to_str(bandwidth, enums.ChannelBandwidthDut)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:CHBW {param}')

	def get_csr(self) -> bool:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:CSR \n
		Snippet: value: bool = driver.configure.connection.hetf.get_csr() \n
		Specifies, whether the check of medium status is required before responding. \n
			:return: required: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:CSR?')
		return Conversions.str_to_bool(response)

	def set_csr(self, required: bool) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:CSR \n
		Snippet: driver.configure.connection.hetf.set_csr(required = False) \n
		Specifies, whether the check of medium status is required before responding. \n
			:param required: OFF | ON
		"""
		param = Conversions.bool_to_str(required)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:CSR {param}')

	def get_nof_symbols(self) -> int:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:NOFSymbols \n
		Snippet: value: int = driver.configure.connection.hetf.get_nof_symbols() \n
		Specifies the length of the HE TB PPDU. \n
			:return: num_of_symbols: integer Range: 1 to 330, Unit: symbol
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:NOFSymbols?')
		return Conversions.str_to_int(response)

	def set_nof_symbols(self, num_of_symbols: int) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:NOFSymbols \n
		Snippet: driver.configure.connection.hetf.set_nof_symbols(num_of_symbols = 1) \n
		Specifies the length of the HE TB PPDU. \n
			:param num_of_symbols: integer Range: 1 to 330, Unit: symbol
		"""
		param = Conversions.decimal_value_to_str(num_of_symbols)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:NOFSymbols {param}')

	# noinspection PyTypeChecker
	def get_ttyp(self) -> enums.TriggerType:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:TTYP \n
		Snippet: value: enums.TriggerType = driver.configure.connection.hetf.get_ttyp() \n
		Specifies the trigger type as specified in the Common Info field. \n
			:return: type_py: BTR | BRP | MRTS | BSRP | BQRP BTR: Basic Trigger BRP: Beamforming Report Poll MRTS: MU-RTS BSRP: Buffer Status Report Poll BQRP: Bandwidth Query Report Poll
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:TTYP?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerType)

	def set_ttyp(self, type_py: enums.TriggerType) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:TTYP \n
		Snippet: driver.configure.connection.hetf.set_ttyp(type_py = enums.TriggerType.BQRP) \n
		Specifies the trigger type as specified in the Common Info field. \n
			:param type_py: BTR | BRP | MRTS | BSRP | BQRP BTR: Basic Trigger BRP: Beamforming Report Poll MRTS: MU-RTS BSRP: Buffer Status Report Poll BQRP: Bandwidth Query Report Poll
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.TriggerType)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:TTYP {param}')

	# noinspection PyTypeChecker
	class TrssiStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Int_Value: int: decimal Target_RSSI index 0 to 90: map to -110 dBm to -20 dBm 91-126: reserved 127: station is commanded to transmit at maximum power for the assigned MCS Range: 0 to 127
			- Dbm_Value: int: decimal Target_RSSI value Range: -110 dBm to -20 dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Int_Value'),
			ArgStruct.scalar_int('Dbm_Value')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Int_Value: int = None
			self.Dbm_Value: int = None

	def get_trssi(self) -> TrssiStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:TRSSi \n
		Snippet: value: TrssiStruct = driver.configure.connection.hetf.get_trssi() \n
		Specifies the expected Rx power of HE TB PPDU transmission as a response to trigger frame. \n
			:return: structure: for return value, see the help for TrssiStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:TRSSi?', self.__class__.TrssiStruct())

	# noinspection PyTypeChecker
	def get_trs_mode(self) -> enums.TriggerFrmPowerMode:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:TRSMode \n
		Snippet: value: enums.TriggerFrmPowerMode = driver.configure.connection.hetf.get_trs_mode() \n
		Specifies the trigger frame power control mode. \n
			:return: mode: AUTO | MANual | MAXPower AUTO: AP_TX_Power and Target_RSSI calculated automatically MAN: The value Target RSSI Control defines adjustment to the Target_RSSI calculation MAXP: Sets the Target_RSSI to 127, the UE transmits the HE TB PPDU at maximum Tx power
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:TRSMode?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerFrmPowerMode)

	def set_trs_mode(self, mode: enums.TriggerFrmPowerMode) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:TRSMode \n
		Snippet: driver.configure.connection.hetf.set_trs_mode(mode = enums.TriggerFrmPowerMode.AUTO) \n
		Specifies the trigger frame power control mode. \n
			:param mode: AUTO | MANual | MAXPower AUTO: AP_TX_Power and Target_RSSI calculated automatically MAN: The value Target RSSI Control defines adjustment to the Target_RSSI calculation MAXP: Sets the Target_RSSI to 127, the UE transmits the HE TB PPDU at maximum Tx power
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.TriggerFrmPowerMode)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:TRSMode {param}')

	def get_tsr_control(self) -> int:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:TSRControl \n
		Snippet: value: int = driver.configure.connection.hetf.get_tsr_control() \n
		Specifies the value Target RSSI Control for adjustment to the Target_RSSI. This parameter is only relevant in manual mode
		for target RSSI calculation. \n
			:return: pwr_db: integer Range: -40 dB to 0 dB
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:TSRControl?')
		return Conversions.str_to_int(response)

	def set_tsr_control(self, pwr_db: int) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HETF:TSRControl \n
		Snippet: driver.configure.connection.hetf.set_tsr_control(pwr_db = 1) \n
		Specifies the value Target RSSI Control for adjustment to the Target_RSSI. This parameter is only relevant in manual mode
		for target RSSI calculation. \n
			:param pwr_db: integer Range: -40 dB to 0 dB
		"""
		param = Conversions.decimal_value_to_str(pwr_db)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HETF:TSRControl {param}')

	def clone(self) -> 'Hetf':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hetf(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
