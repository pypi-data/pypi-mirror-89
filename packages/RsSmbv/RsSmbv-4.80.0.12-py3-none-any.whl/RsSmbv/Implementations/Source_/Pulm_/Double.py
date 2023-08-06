from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Double:
	"""Double commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("double", core, parent)

	def get_delay(self) -> float:
		"""SCPI: [SOURce<HW>]:PULM:DOUBle:DELay \n
		Snippet: value: float = driver.source.pulm.double.get_delay() \n
		Sets the delay from the start of the first pulse to the start of the second pulse. \n
			:return: delay: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:DOUBle:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""SCPI: [SOURce<HW>]:PULM:DOUBle:DELay \n
		Snippet: driver.source.pulm.double.set_delay(delay = 1.0) \n
		Sets the delay from the start of the first pulse to the start of the second pulse. \n
			:param delay: float
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:PULM:DOUBle:DELay {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:PULM:DOUBle:STATe \n
		Snippet: value: bool = driver.source.pulm.double.get_state() \n
		Provided for backward compatibility with former Rohde & Schwarz signal generators. Works like the command method RsSmbv.
		Source.Pulm.modeDOUBle. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:DOUBle:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:PULM:DOUBle:STATe \n
		Snippet: driver.source.pulm.double.set_state(state = False) \n
		Provided for backward compatibility with former Rohde & Schwarz signal generators. Works like the command method RsSmbv.
		Source.Pulm.modeDOUBle. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:PULM:DOUBle:STATe {param}')

	def get_width(self) -> float:
		"""SCPI: [SOURce<HW>]:PULM:DOUBle:WIDTh \n
		Snippet: value: float = driver.source.pulm.double.get_width() \n
		Sets the width of the second pulse. \n
			:return: width: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:DOUBle:WIDTh?')
		return Conversions.str_to_float(response)

	def set_width(self, width: float) -> None:
		"""SCPI: [SOURce<HW>]:PULM:DOUBle:WIDTh \n
		Snippet: driver.source.pulm.double.set_width(width = 1.0) \n
		Sets the width of the second pulse. \n
			:param width: float
		"""
		param = Conversions.decimal_value_to_str(width)
		self._core.io.write(f'SOURce<HwInstance>:PULM:DOUBle:WIDTh {param}')
