from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Execute:
	"""Execute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("execute", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:COPY:EXECute \n
		Snippet: driver.source.bb.w3Gpp.copy.execute.set() \n
		The command starts the copy process. The dataset of the source station is copied to the destination station. Whether the
		data is copied to a base station or a user equipment depends on which transmission direction is selected (command
		W3GPp:LINK UP | DOWN) . \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:COPY:EXECute')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:COPY:EXECute \n
		Snippet: driver.source.bb.w3Gpp.copy.execute.set_with_opc() \n
		The command starts the copy process. The dataset of the source station is copied to the destination station. Whether the
		data is copied to a base station or a user equipment depends on which transmission direction is selected (command
		W3GPp:LINK UP | DOWN) . \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:W3GPp:COPY:EXECute')
