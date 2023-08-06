from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Restart:
	"""Restart commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("restart", core, parent)

	def set(self) -> None:
		"""SCPI: SYSTem:COMMunicate:NETWork:RESTart \n
		Snippet: driver.system.communicate.network.restart.set() \n
		Restarts the network. \n
		"""
		self._core.io.write(f'SYSTem:COMMunicate:NETWork:RESTart')

	def set_with_opc(self) -> None:
		"""SCPI: SYSTem:COMMunicate:NETWork:RESTart \n
		Snippet: driver.system.communicate.network.restart.set_with_opc() \n
		Restarts the network. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:COMMunicate:NETWork:RESTart')
