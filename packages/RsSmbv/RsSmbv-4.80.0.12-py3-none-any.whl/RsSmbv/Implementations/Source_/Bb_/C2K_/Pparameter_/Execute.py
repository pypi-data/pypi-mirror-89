from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Execute:
	"""Execute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("execute", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:C2K:PPARameter:EXECute \n
		Snippet: driver.source.bb.c2K.pparameter.execute.set() \n
		This command presets the channel table of base station 1 with the parameters defined by the PPARameter commands. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:PPARameter:EXECute')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:C2K:PPARameter:EXECute \n
		Snippet: driver.source.bb.c2K.pparameter.execute.set_with_opc() \n
		This command presets the channel table of base station 1 with the parameters defined by the PPARameter commands. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:C2K:PPARameter:EXECute')
