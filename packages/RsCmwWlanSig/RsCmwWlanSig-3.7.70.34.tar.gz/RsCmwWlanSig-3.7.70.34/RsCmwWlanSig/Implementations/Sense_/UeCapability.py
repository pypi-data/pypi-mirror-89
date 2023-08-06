from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UeCapability:
	"""UeCapability commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ueCapability", core, parent)

	@property
	def mac(self):
		"""mac commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mac'):
			from .UeCapability_.Mac import Mac
			self._mac = Mac(self._core, self._base)
		return self._mac

	# noinspection PyTypeChecker
	class HeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Device_Class: enums.DeviceClass: A | B
			- Dyn_Fragment: enums.DynFragment: NO | L1 | L2 | L3 Dynamic fragmentation not supported, or dynamic fragmentation supported with level 1 to 3.
			- Absr: enums.YesNoStatus: NO | YES Indicates support of a buffer status report (BSR) control field.
			- Broadcast_Twt: enums.YesNoStatus: NO | YES Indicates support of broadcast target wake time (TWT) operation.
			- Ofdm_Arand_Acc: enums.YesNoStatus: NO | YES Indicates support of OFDMA random access procedure."""
		__meta_args_list = [
			ArgStruct.scalar_enum('Device_Class', enums.DeviceClass),
			ArgStruct.scalar_enum('Dyn_Fragment', enums.DynFragment),
			ArgStruct.scalar_enum('Absr', enums.YesNoStatus),
			ArgStruct.scalar_enum('Broadcast_Twt', enums.YesNoStatus),
			ArgStruct.scalar_enum('Ofdm_Arand_Acc', enums.YesNoStatus)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Device_Class: enums.DeviceClass = None
			self.Dyn_Fragment: enums.DynFragment = None
			self.Absr: enums.YesNoStatus = None
			self.Broadcast_Twt: enums.YesNoStatus = None
			self.Ofdm_Arand_Acc: enums.YesNoStatus = None

	# noinspection PyTypeChecker
	def get_he(self) -> HeStruct:
		"""SCPI: SENSe:WLAN:SIGNaling<instance>:UECapability:HE \n
		Snippet: value: HeStruct = driver.sense.ueCapability.get_he() \n
		Indicates the reported UE HE capabilities. \n
			:return: structure: for return value, see the help for HeStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:WLAN:SIGNaling<Instance>:UECapability:HE?', self.__class__.HeStruct())

	def clone(self) -> 'UeCapability':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UeCapability(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
