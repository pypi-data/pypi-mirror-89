from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Throughput:
	"""Throughput commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("throughput", core, parent)

	def get_delay(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DM:SMODulation:THRoughput:DELay \n
		Snippet: value: int = driver.source.bb.dm.smodulation.throughput.get_delay() \n
		No command help available \n
			:return: delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:SMODulation:THRoughput:DELay?')
		return Conversions.str_to_int(response)
