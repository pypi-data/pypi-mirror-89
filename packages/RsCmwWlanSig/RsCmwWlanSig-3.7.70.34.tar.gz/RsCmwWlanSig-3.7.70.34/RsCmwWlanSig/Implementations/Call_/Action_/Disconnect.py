from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Disconnect:
	"""Disconnect commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("disconnect", core, parent)

	def set(self) -> None:
		"""SCPI: CALL:WLAN:SIGNaling<Instance>:ACTion:DISConnect \n
		Snippet: driver.call.action.disconnect.set() \n
		Disassociates and deauthenticates the DUT by sending a deauthentication frame. \n
		"""
		self._core.io.write(f'CALL:WLAN:SIGNaling<Instance>:ACTion:DISConnect')

	def set_with_opc(self) -> None:
		"""SCPI: CALL:WLAN:SIGNaling<Instance>:ACTion:DISConnect \n
		Snippet: driver.call.action.disconnect.set_with_opc() \n
		Disassociates and deauthenticates the DUT by sending a deauthentication frame. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwWlanSig.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CALL:WLAN:SIGNaling<Instance>:ACTion:DISConnect')
