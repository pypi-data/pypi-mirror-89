from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Static:
	"""Static commands group definition. 7 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("static", core, parent)

	@property
	def ipAddress(self):
		"""ipAddress commands group. 0 Sub-classes, 6 commands."""
		if not hasattr(self, '_ipAddress'):
			from .Static_.IpAddress import IpAddress
			self._ipAddress = IpAddress(self._core, self._base)
		return self._ipAddress

	# noinspection PyTypeChecker
	class SmaskStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- First_Octet: int: No parameter help available
			- Second_Octet: int: No parameter help available
			- Third_Octet: int: No parameter help available
			- Fourth_Octet: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('First_Octet'),
			ArgStruct.scalar_int('Second_Octet'),
			ArgStruct.scalar_int('Third_Octet'),
			ArgStruct.scalar_int('Fourth_Octet')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.First_Octet: int = None
			self.Second_Octet: int = None
			self.Third_Octet: int = None
			self.Fourth_Octet: int = None

	def get_smask(self) -> SmaskStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:STATic:SMASk \n
		Snippet: value: SmaskStruct = driver.configure.ipv4.static.get_smask() \n
		Specifies the subnet mask of the built-in IPv4 stack. The setting is relevant for instruments without DAU. \n
			:return: structure: for return value, see the help for SmaskStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:IPVFour:STATic:SMASk?', self.__class__.SmaskStruct())

	def set_smask(self, value: SmaskStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:STATic:SMASk \n
		Snippet: driver.configure.ipv4.static.set_smask(value = SmaskStruct()) \n
		Specifies the subnet mask of the built-in IPv4 stack. The setting is relevant for instruments without DAU. \n
			:param value: see the help for SmaskStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:IPVFour:STATic:SMASk', value)

	def clone(self) -> 'Static':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Static(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
