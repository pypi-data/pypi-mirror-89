from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InputPy:
	"""InputPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("inputPy", core, parent)

	def get_frequency(self) -> float:
		"""SCPI: CLOCk:INPut:FREQuency \n
		Snippet: value: float = driver.clock.inputPy.get_frequency() \n
		No command help available \n
			:return: frequency: No help available
		"""
		response = self._core.io.query_str('CLOCk:INPut:FREQuency?')
		return Conversions.str_to_float(response)
