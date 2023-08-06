from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Connection:
	"""Connection commands group definition. 104 total commands, 15 Sub-groups, 17 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("connection", core, parent)

	@property
	def hotspot(self):
		"""hotspot commands group. 3 Sub-classes, 4 commands."""
		if not hasattr(self, '_hotspot'):
			from .Connection_.Hotspot import Hotspot
			self._hotspot = Hotspot(self._core, self._base)
		return self._hotspot

	@property
	def wdirect(self):
		"""wdirect commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_wdirect'):
			from .Connection_.Wdirect import Wdirect
			self._wdirect = Wdirect(self._core, self._base)
		return self._wdirect

	@property
	def station(self):
		"""station commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_station'):
			from .Connection_.Station import Station
			self._station = Station(self._core, self._base)
		return self._station

	@property
	def security(self):
		"""security commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_security'):
			from .Connection_.Security import Security
			self._security = Security(self._core, self._base)
		return self._security

	@property
	def qos(self):
		"""qos commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_qos'):
			from .Connection_.Qos import Qos
			self._qos = Qos(self._core, self._base)
		return self._qos

	@property
	def srates(self):
		"""srates commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_srates'):
			from .Connection_.Srates import Srates
			self._srates = Srates(self._core, self._base)
		return self._srates

	@property
	def dframe(self):
		"""dframe commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dframe'):
			from .Connection_.Dframe import Dframe
			self._dframe = Dframe(self._core, self._base)
		return self._dframe

	@property
	def hetf(self):
		"""hetf commands group. 1 Sub-classes, 19 commands."""
		if not hasattr(self, '_hetf'):
			from .Connection_.Hetf import Hetf
			self._hetf = Hetf(self._core, self._base)
		return self._hetf

	@property
	def ccode(self):
		"""ccode commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ccode'):
			from .Connection_.Ccode import Ccode
			self._ccode = Ccode(self._core, self._base)
		return self._ccode

	@property
	def edca(self):
		"""edca commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_edca'):
			from .Connection_.Edca import Edca
			self._edca = Edca(self._core, self._base)
		return self._edca

	@property
	def muedca(self):
		"""muedca commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_muedca'):
			from .Connection_.Muedca import Muedca
			self._muedca = Muedca(self._core, self._base)
		return self._muedca

	@property
	def hemac(self):
		"""hemac commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hemac'):
			from .Connection_.Hemac import Hemac
			self._hemac = Hemac(self._core, self._base)
		return self._hemac

	@property
	def ndpSounding(self):
		"""ndpSounding commands group. 1 Sub-classes, 9 commands."""
		if not hasattr(self, '_ndpSounding'):
			from .Connection_.NdpSounding import NdpSounding
			self._ndpSounding = NdpSounding(self._core, self._base)
		return self._ndpSounding

	@property
	def twt(self):
		"""twt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_twt'):
			from .Connection_.Twt import Twt
			self._twt = Twt(self._core, self._base)
		return self._twt

	@property
	def btwt(self):
		"""btwt commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_btwt'):
			from .Connection_.Btwt import Btwt
			self._btwt = Btwt(self._core, self._base)
		return self._btwt

	# noinspection PyTypeChecker
	def get_iv_support(self) -> enums.IpVersionExt:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:IVSupport \n
		Snippet: value: enums.IpVersionExt = driver.configure.connection.get_iv_support() \n
		Defines the required IP version support. \n
			:return: version: IV4 | IV6 | IV4V6 IPv4 only, IPv6 only, or both
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:IVSupport?')
		return Conversions.str_to_scalar_enum(response, enums.IpVersionExt)

	def set_iv_support(self, version: enums.IpVersionExt) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:IVSupport \n
		Snippet: driver.configure.connection.set_iv_support(version = enums.IpVersionExt.IV4) \n
		Defines the required IP version support. \n
			:param version: IV4 | IV6 | IV4V6 IPv4 only, IPv6 only, or both
		"""
		param = Conversions.enum_scalar_to_str(version, enums.IpVersionExt)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:IVSupport {param}')

	# noinspection PyTypeChecker
	def get_omode(self) -> enums.EntityOperationMode:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:OMODe \n
		Snippet: value: enums.EntityOperationMode = driver.configure.connection.get_omode() \n
		Selects the operation mode, that is the type of WLAN entity simulated by the WLAN signaling application. \n
			:return: mode: AP | STATion | HSPot2 AP: access point in infrastructure mode STATion: WLAN station HSPot2: WiFi Hotspot 2.0 access point
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:OMODe?')
		return Conversions.str_to_scalar_enum(response, enums.EntityOperationMode)

	def set_omode(self, mode: enums.EntityOperationMode) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:OMODe \n
		Snippet: driver.configure.connection.set_omode(mode = enums.EntityOperationMode.AP) \n
		Selects the operation mode, that is the type of WLAN entity simulated by the WLAN signaling application. \n
			:param mode: AP | STATion | HSPot2 AP: access point in infrastructure mode STATion: WLAN station HSPot2: WiFi Hotspot 2.0 access point
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.EntityOperationMode)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:OMODe {param}')

	# noinspection PyTypeChecker
	def get_smoothing(self) -> enums.SmoothingBit:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SMOothing \n
		Snippet: value: enums.SmoothingBit = driver.configure.connection.get_smoothing() \n
		Indicates to the receiver whether the frequency-domain smoothing is recommended for channel estimation. \n
			:return: bit: NRECommended | RECommended Not recommended or recommended
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SMOothing?')
		return Conversions.str_to_scalar_enum(response, enums.SmoothingBit)

	def set_smoothing(self, bit: enums.SmoothingBit) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SMOothing \n
		Snippet: driver.configure.connection.set_smoothing(bit = enums.SmoothingBit.NRECommended) \n
		Indicates to the receiver whether the frequency-domain smoothing is recommended for channel estimation. \n
			:param bit: NRECommended | RECommended Not recommended or recommended
		"""
		param = Conversions.enum_scalar_to_str(bit, enums.SmoothingBit)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:SMOothing {param}')

	def get_pa_interrupt(self) -> bool:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:PAINterrupt \n
		Snippet: value: bool = driver.configure.connection.get_pa_interrupt() \n
		No command help available \n
			:return: enable: No help available
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:PAINterrupt?')
		return Conversions.str_to_bool(response)

	def set_pa_interrupt(self, enable: bool) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:PAINterrupt \n
		Snippet: driver.configure.connection.set_pa_interrupt(enable = False) \n
		No command help available \n
			:param enable: No help available
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:PAINterrupt {param}')

	# noinspection PyTypeChecker
	class MfDefStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- State: enums.EnableState: DISable | ENABle Disables/enables the user-defined frame rate control
			- Format_Py: enums.DataFormatExt: NHT | HTM | VHT | HES | HEM Selects the frame format NHT: non-high throughput format (non-HT) HTM: HT mixed format (HT MF) VHT: very high throughput format HES: high efficiency single-user format (HE SU) HEM: high efficiency multi-user format (HE MU)
			- Rate: enums.CodeRate: D1MBit | D2MBits | C55Mbits | C11Mbits | BR12 | BR34 | QR12 | QR34 | Q1M12 | Q1M34 | Q6M23 | Q6M34 | MCS | MCS1 | MCS2 | MCS3 | MCS4 | MCS5 | MCS6 | MCS7 | MCS8 | MCS9 | MCS10 | MCS11 | MCS12 | MCS13 | MCS14 | MCS15 Sets the rate D1MBit: DSSS, 1 Mbit/s D2MBits: DSSS, 2 Mbit/s C55Mbits: CCK, 5.5 Mbit/s C11Mbits: CCK, 11 Mbit/s BR12: BPSK, 1/2, 6 Mbit/s BR34: BPSK, 3/4, 9 Mbit/s QR12: QPSK, 1/2, 12 Mbit/s QR34: QPSK, 3/4, 18 Mbit/s Q1M12: 16-QAM, 1/2, 24 Mbit/s Q1M34: 16-QAM, 3/4, 36 Mbit/s Q6M23: 64-QAM, 2/3, 48 Mbit/s Q6M34: 64-QAM, 3/4, 54 Mbit/s MCS, MCS1,...,MCS15: MCS 0 to MCS 15"""
		__meta_args_list = [
			ArgStruct.scalar_enum('State', enums.EnableState),
			ArgStruct.scalar_enum('Format_Py', enums.DataFormatExt),
			ArgStruct.scalar_enum('Rate', enums.CodeRate)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.State: enums.EnableState = None
			self.Format_Py: enums.DataFormatExt = None
			self.Rate: enums.CodeRate = None

	# noinspection PyTypeChecker
	def get_mf_def(self) -> MfDefStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:MFDef \n
		Snippet: value: MfDefStruct = driver.configure.connection.get_mf_def() \n
		Enables and configures the user-defined frame rate control for management frames. \n
			:return: structure: for return value, see the help for MfDefStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:MFDef?', self.__class__.MfDefStruct())

	def set_mf_def(self, value: MfDefStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:MFDef \n
		Snippet: driver.configure.connection.set_mf_def(value = MfDefStruct()) \n
		Enables and configures the user-defined frame rate control for management frames. \n
			:param value: see the help for MfDefStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:MFDef', value)

	# noinspection PyTypeChecker
	class DfdefStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- State: enums.EnableState: DISable | ENABle Disables/enables the user-defined frame rate control
			- Format_Py: enums.DataFormatExt: NHT | HTM | VHT | HES | HEM Selects the frame format NHT: non-high throughput format (non-HT) HTM: HT mixed format (HT MF) VHT: very high throughput format HES: high efficiency single-user format (HE SU) HEM: high efficiency multi-user format (HE MU)
			- Chan_Bw: enums.ChannelBandwidthDut: BW20 | BW40 | BW80 | BW160 Channel bandwidth The value must not exceed the operating channel bandwidth, see [CMDLINK: CONFigure:WLAN:SIGNi:RFSettings:OCWidth CMDLINK].
			- Rate: enums.CodeRate: D1MBit | D2MBits | C55Mbits | C11Mbits | BR12 | BR34 | QR12 | QR34 | Q1M12 | Q1M34 | Q6M23 | Q6M34 | MCS | MCS1 | MCS2 | MCS3 | MCS4 | MCS5 | MCS6 | MCS7 | MCS8 | MCS9 | MCS10 | MCS11 | MCS12 | MCS13 | MCS14 | MCS15 See rate list in [CMDLINK: CONFigure:WLAN:SIGNi:CONNection:MFDef CMDLINK]
			- Guard_Interval: enums.GuardInterval: LONG | SHORt | GI08 | GI16 | GI32 SHORt, LONG: short or long guard interval (up to IEEE 802.11ac) GI08, GI16, GI32: 0.8 μs, 1.6 μs, and 3.2 μs guard interval durations (for IEEE 802.11ax)
			- Lt_Ftype: enums.LtfType: X1 | X2 | X4 1x LTF, 2x LTF, 4x LTF for 802.11ax
			- Pe_Duration: enums.PeDuration: PE0 | PE4 | PE8 | PE12 | PE16 | AUTO PEx: additional receive processing time of x μs signaled in packet extension (PE) field (only for IEEE 802.11ax) AUTO: automatic setting based on the reported DUTs capabilities
			- Ctype: enums.CodingType: LDPC | BCC Coding type (for IEEE 802.11ax - VHT, HE_SU, HE_MU frames only) : low density parity check or binary convolution code
			- Streams: enums.Streams: STR1 | STR2 Number of streams
			- Stbc: bool: OFF | ON Enables / disables space time block coding (STBC) . If disabled, spatial multiplexing is used."""
		__meta_args_list = [
			ArgStruct.scalar_enum('State', enums.EnableState),
			ArgStruct.scalar_enum('Format_Py', enums.DataFormatExt),
			ArgStruct.scalar_enum('Chan_Bw', enums.ChannelBandwidthDut),
			ArgStruct.scalar_enum('Rate', enums.CodeRate),
			ArgStruct.scalar_enum('Guard_Interval', enums.GuardInterval),
			ArgStruct.scalar_enum('Lt_Ftype', enums.LtfType),
			ArgStruct.scalar_enum('Pe_Duration', enums.PeDuration),
			ArgStruct.scalar_enum('Ctype', enums.CodingType),
			ArgStruct.scalar_enum('Streams', enums.Streams),
			ArgStruct.scalar_bool('Stbc')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.State: enums.EnableState = None
			self.Format_Py: enums.DataFormatExt = None
			self.Chan_Bw: enums.ChannelBandwidthDut = None
			self.Rate: enums.CodeRate = None
			self.Guard_Interval: enums.GuardInterval = None
			self.Lt_Ftype: enums.LtfType = None
			self.Pe_Duration: enums.PeDuration = None
			self.Ctype: enums.CodingType = None
			self.Streams: enums.Streams = None
			self.Stbc: bool = None

	# noinspection PyTypeChecker
	def get_dfdef(self) -> DfdefStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:DFDef \n
		Snippet: value: DfdefStruct = driver.configure.connection.get_dfdef() \n
		Enables and configures the user-defined frame rate control for data frames. \n
			:return: structure: for return value, see the help for DfdefStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:DFDef?', self.__class__.DfdefStruct())

	def set_dfdef(self, value: DfdefStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:DFDef \n
		Snippet: driver.configure.connection.set_dfdef(value = DfdefStruct()) \n
		Enables and configures the user-defined frame rate control for data frames. \n
			:param value: see the help for DfdefStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:DFDef', value)

	def get_sync(self) -> bool:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SYNC \n
		Snippet: value: bool = driver.configure.connection.get_sync() \n
		If enabled, the PER measurements use identical settings as configured in the signaling application. Refer to the 'Data
		Frame Control Settings'. \n
			:return: sync: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SYNC?')
		return Conversions.str_to_bool(response)

	def set_sync(self, sync: bool) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SYNC \n
		Snippet: driver.configure.connection.set_sync(sync = False) \n
		If enabled, the PER measurements use identical settings as configured in the signaling application. Refer to the 'Data
		Frame Control Settings'. \n
			:param sync: OFF | ON
		"""
		param = Conversions.bool_to_str(sync)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:SYNC {param}')

	def get_ssid(self) -> str:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SSID \n
		Snippet: value: str = driver.configure.connection.get_ssid() \n
		Sets the service set identifier (SSID) . \n
			:return: ssid: string String with up to 32 characters (7-bit ASCII only)
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SSID?')
		return trim_str_response(response)

	def set_ssid(self, ssid: str) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SSID \n
		Snippet: driver.configure.connection.set_ssid(ssid = '1') \n
		Sets the service set identifier (SSID) . \n
			:param ssid: string String with up to 32 characters (7-bit ASCII only)
		"""
		param = Conversions.value_to_quoted_str(ssid)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:SSID {param}')

	# noinspection PyTypeChecker
	class AidStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Start: int: numeric Range: 1 to 2007
			- Stop: int: numeric Range: 1 to 2007"""
		__meta_args_list = [
			ArgStruct.scalar_int('Start'),
			ArgStruct.scalar_int('Stop')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Start: int = None
			self.Stop: int = None

	def get_aid(self) -> AidStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:AID \n
		Snippet: value: AidStruct = driver.configure.connection.get_aid() \n
		Specifies the range of IDs to be assigned by the access point to the connected DUTs. \n
			:return: structure: for return value, see the help for AidStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:AID?', self.__class__.AidStruct())

	def set_aid(self, value: AidStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:AID \n
		Snippet: driver.configure.connection.set_aid(value = AidStruct()) \n
		Specifies the range of IDs to be assigned by the access point to the connected DUTs. \n
			:param value: see the help for AidStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:AID', value)

	def get_bss_color(self) -> int:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:BSSColor \n
		Snippet: value: int = driver.configure.connection.get_bss_color() \n
		Specifies the color code of basic service set (BSS) . \n
			:return: value: numeric Range: 1 to 63
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:BSSColor?')
		return Conversions.str_to_int(response)

	def set_bss_color(self, value: int) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:BSSColor \n
		Snippet: driver.configure.connection.set_bss_color(value = 1) \n
		Specifies the color code of basic service set (BSS) . \n
			:param value: numeric Range: 1 to 63
		"""
		param = Conversions.decimal_value_to_str(value)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:BSSColor {param}')

	def get_bssid(self) -> str:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:BSSid \n
		Snippet: value: str = driver.configure.connection.get_bssid() \n
		Sets the 48-bit MAC address of the WLAN interface. \n
			:return: bssid: hex Hexadecimal number with 12 digits Leading zeros can be omitted. Range: #H0 to #HFFFFFFFFFFFF
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:BSSid?')
		return trim_str_response(response)

	def set_bssid(self, bssid: str) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:BSSid \n
		Snippet: driver.configure.connection.set_bssid(bssid = r1) \n
		Sets the 48-bit MAC address of the WLAN interface. \n
			:param bssid: hex Hexadecimal number with 12 digits Leading zeros can be omitted. Range: #H0 to #HFFFFFFFFFFFF
		"""
		param = Conversions.value_to_str(bssid)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:BSSid {param}')

	def get_beacon(self) -> int:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:BEACon \n
		Snippet: value: int = driver.configure.connection.get_beacon() \n
		Sets the interval between two beacon frame transmissions for a simulated infrastructure/ ad-hoc network. \n
			:return: beacon_intervall: integer Interval in time units (1 TU = 1024 µs) Range: 20 to 16000
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:BEACon?')
		return Conversions.str_to_int(response)

	def set_beacon(self, beacon_intervall: int) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:BEACon \n
		Snippet: driver.configure.connection.set_beacon(beacon_intervall = 1) \n
		Sets the interval between two beacon frame transmissions for a simulated infrastructure/ ad-hoc network. \n
			:param beacon_intervall: integer Interval in time units (1 TU = 1024 µs) Range: 20 to 16000
		"""
		param = Conversions.decimal_value_to_str(beacon_intervall)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:BEACon {param}')

	def get_dperiod(self) -> int:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:DPERiod \n
		Snippet: value: int = driver.configure.connection.get_dperiod() \n
		Sets the number of beacon intervals between successive delivery traffic indication messages (DTIM) . \n
			:return: period: integer Number of beacon intervals Range: 1 to 10
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:DPERiod?')
		return Conversions.str_to_int(response)

	def set_dperiod(self, period: int) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:DPERiod \n
		Snippet: driver.configure.connection.set_dperiod(period = 1) \n
		Sets the number of beacon intervals between successive delivery traffic indication messages (DTIM) . \n
			:param period: integer Number of beacon intervals Range: 1 to 10
		"""
		param = Conversions.decimal_value_to_str(period)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:DPERiod {param}')

	# noinspection PyTypeChecker
	def get_standard(self) -> enums.StandardType:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:STANdard \n
		Snippet: value: enums.StandardType = driver.configure.connection.get_standard() \n
		Selects the IEEE 802.11 WLAN standard to be used. \n
			:return: typ: ASTD | GOSTd | ANSTd | GONStd | BSTD | GSTD | GNSTd | ACSTd | AXSTd BSTD: 802.11b ASTD: 802.11a GSTD: 802.11g GOSTd: 802.11g (OFDM) ANSTd: 802.11a/n GNSTd: 802.11g/n GONStd: 802.11g (OFDM) /n ACSTd: 802.11ac AXSTd: 802.11ax
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:STANdard?')
		return Conversions.str_to_scalar_enum(response, enums.StandardType)

	def set_standard(self, typ: enums.StandardType) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:STANdard \n
		Snippet: driver.configure.connection.set_standard(typ = enums.StandardType.ACSTd) \n
		Selects the IEEE 802.11 WLAN standard to be used. \n
			:param typ: ASTD | GOSTd | ANSTd | GONStd | BSTD | GSTD | GNSTd | ACSTd | AXSTd BSTD: 802.11b ASTD: 802.11a GSTD: 802.11g GOSTd: 802.11g (OFDM) ANSTd: 802.11a/n GNSTd: 802.11g/n GONStd: 802.11g (OFDM) /n ACSTd: 802.11ac AXSTd: 802.11ax
		"""
		param = Conversions.enum_scalar_to_str(typ, enums.StandardType)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:STANdard {param}')

	# noinspection PyTypeChecker
	class AmpduStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: enums.EnableState: DISable | ENABle Enables/ disables the A-MPDUs
			- Multi_Tid: enums.EnableState: DISable | ENABle Enables/ disables multi-TID A-MPDU
			- Max_Length: int: integer The maximal length of entire A-MPDU Range: 50 to 131.071E+3, Unit: byte"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Enable', enums.EnableState),
			ArgStruct.scalar_enum('Multi_Tid', enums.EnableState),
			ArgStruct.scalar_int('Max_Length')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: enums.EnableState = None
			self.Multi_Tid: enums.EnableState = None
			self.Max_Length: int = None

	# noinspection PyTypeChecker
	def get_ampdu(self) -> AmpduStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:AMPDu \n
		Snippet: value: AmpduStruct = driver.configure.connection.get_ampdu() \n
		Configures aggregate MPDUs (A-MPDU) . \n
			:return: structure: for return value, see the help for AmpduStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:AMPDu?', self.__class__.AmpduStruct())

	def set_ampdu(self, value: AmpduStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:AMPDu \n
		Snippet: driver.configure.connection.set_ampdu(value = AmpduStruct()) \n
		Configures aggregate MPDUs (A-MPDU) . \n
			:param value: see the help for AmpduStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:AMPDu', value)

	# noinspection PyTypeChecker
	class DyFragmentStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Level: enums.Level: No parameter help available
			- Enable_Tx: enums.EnableState: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Level', enums.Level),
			ArgStruct.scalar_enum('Enable_Tx', enums.EnableState)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Level: enums.Level = None
			self.Enable_Tx: enums.EnableState = None

	# noinspection PyTypeChecker
	def get_dy_fragment(self) -> DyFragmentStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:DYFRagment \n
		Snippet: value: DyFragmentStruct = driver.configure.connection.get_dy_fragment() \n
		No command help available \n
			:return: structure: for return value, see the help for DyFragmentStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:DYFRagment?', self.__class__.DyFragmentStruct())

	def set_dy_fragment(self, value: DyFragmentStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:DYFRagment \n
		Snippet: driver.configure.connection.set_dy_fragment(value = DyFragmentStruct()) \n
		No command help available \n
			:param value: see the help for DyFragmentStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:DYFRagment', value)

	def get_dsss(self) -> bool:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:DSSS \n
		Snippet: value: bool = driver.configure.connection.get_dsss() \n
		No command help available \n
			:return: support_of_dsss: No help available
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:DSSS?')
		return Conversions.str_to_bool(response)

	def set_dsss(self, support_of_dsss: bool) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:DSSS \n
		Snippet: driver.configure.connection.set_dsss(support_of_dsss = False) \n
		No command help available \n
			:param support_of_dsss: No help available
		"""
		param = Conversions.bool_to_str(support_of_dsss)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:DSSS {param}')

	def clone(self) -> 'Connection':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Connection(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
