from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StaInfo:
	"""StaInfo commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("staInfo", core, parent)

	def get_ap_ssid(self) -> str:
		"""SCPI: SENSe:WLAN:SIGNaling<instance>:STAinfo:APSSid \n
		Snippet: value: str = driver.sense.staInfo.get_ap_ssid() \n
		Returns the SSID of the associated access point. The command is only relevant in operation mode 'Station'. \n
			:return: ssid: string Service set identifier as string
		"""
		response = self._core.io.query_str('SENSe:WLAN:SIGNaling<Instance>:STAinfo:APSSid?')
		return trim_str_response(response)
