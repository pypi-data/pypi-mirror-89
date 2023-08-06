from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mac:
	"""Mac commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mac", core, parent)

	def get_address(self) -> str:
		"""SCPI: SENSe:WLAN:SIGNaling<instance>:UECapability:MAC:ADDRess \n
		Snippet: value: str = driver.sense.ueCapability.mac.get_address() \n
		Gets the MAC address of an associated DUT. \n
			:return: mac_address: string Hexadecimal MAC address as string
		"""
		response = self._core.io.query_str('SENSe:WLAN:SIGNaling<Instance>:UECapability:MAC:ADDRess?')
		return trim_str_response(response)
