from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fpreset:
	"""Fpreset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fpreset", core, parent)

	def set(self) -> None:
		"""SCPI: SYSTem:FPReset \n
		Snippet: driver.system.fpreset.set() \n
		Triggers an instrument reset to the original state of delivery. \n
		"""
		self._core.io.write(f'SYSTem:FPReset')

	def set_with_opc(self) -> None:
		"""SCPI: SYSTem:FPReset \n
		Snippet: driver.system.fpreset.set_with_opc() \n
		Triggers an instrument reset to the original state of delivery. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:FPReset')
