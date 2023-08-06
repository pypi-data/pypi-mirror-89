from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sonce:
	"""Sonce commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sonce", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ALC:SONCe \n
		Snippet: driver.source.power.alc.sonce.set() \n
		Activates level control for correction purposes temporarily. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:POWer:ALC:SONCe')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ALC:SONCe \n
		Snippet: driver.source.power.alc.sonce.set_with_opc() \n
		Activates level control for correction purposes temporarily. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:POWer:ALC:SONCe')
