from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bbin:
	"""Bbin commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bbin", core, parent)

	def get_measure(self) -> bool:
		"""SCPI: CALibration<HW>:BBIN:[MEASure] \n
		Snippet: value: bool = driver.calibration.bbin.get_measure() \n
		No command help available \n
			:return: measure: No help available
		"""
		response = self._core.io.query_str('CALibration<HwInstance>:BBIN:MEASure?')
		return Conversions.str_to_bool(response)
