from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Append:
	"""Append commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("append", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB:APPend \n
		Snippet: driver.source.bb.gbas.vdb.append.set() \n
		Appends a new VDB to the end of the VDB list. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB:APPend')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB:APPend \n
		Snippet: driver.source.bb.gbas.vdb.append.set_with_opc() \n
		Appends a new VDB to the end of the VDB list. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GBAS:VDB:APPend')
