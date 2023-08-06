from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SrData:
	"""SrData commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("srData", core, parent)

	def delete(self) -> None:
		"""SCPI: SYSTem:SRData:DELete \n
		Snippet: driver.system.srData.delete() \n
		No command help available \n
		"""
		self._core.io.write(f'SYSTem:SRData:DELete')

	def delete_with_opc(self) -> None:
		"""SCPI: SYSTem:SRData:DELete \n
		Snippet: driver.system.srData.delete_with_opc() \n
		No command help available \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:SRData:DELete')

	def get_value(self) -> bytes:
		"""SCPI: SYSTem:SRData \n
		Snippet: value: bytes = driver.system.srData.get_value() \n
		Queris the SCPI recording data from the internal file. This feature enables you to transfer an instrument configuration
		to other test environments, as e.g. laboratory virtual instruments. \n
			:return: file_data: block data
		"""
		response = self._core.io.query_bin_block('SYSTem:SRData?')
		return response
