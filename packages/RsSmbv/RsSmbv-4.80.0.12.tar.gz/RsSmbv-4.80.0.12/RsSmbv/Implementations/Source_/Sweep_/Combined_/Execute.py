from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Execute:
	"""Execute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("execute", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:COMBined:EXECute \n
		Snippet: driver.source.sweep.combined.execute.set() \n
		Executes an RF frequency / level sweep cycle. The command triggers one single sweep manually. Therefore, you can use it
		in manual sweep mode, selected with the command [:SOURce<hw>]:SWEep:COMBined:MODE > MANual. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:SWEep:COMBined:EXECute')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:COMBined:EXECute \n
		Snippet: driver.source.sweep.combined.execute.set_with_opc() \n
		Executes an RF frequency / level sweep cycle. The command triggers one single sweep manually. Therefore, you can use it
		in manual sweep mode, selected with the command [:SOURce<hw>]:SWEep:COMBined:MODE > MANual. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:SWEep:COMBined:EXECute')
