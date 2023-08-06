from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Clock:
	"""Clock commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("clock", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ClockModeA:
		"""SCPI: [SOURce<HW>]:BB:WLAN:CLOCk:MODE \n
		Snippet: value: enums.ClockModeA = driver.source.bb.wlan.clock.get_mode() \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:CLOCk:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ClockModeA)

	def set_mode(self, mode: enums.ClockModeA) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:CLOCk:MODE \n
		Snippet: driver.source.bb.wlan.clock.set_mode(mode = enums.ClockModeA.CHIP) \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ClockModeA)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:CLOCk:MODE {param}')

	def get_multiplier(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:WLAN:CLOCk:MULTiplier \n
		Snippet: value: float = driver.source.bb.wlan.clock.get_multiplier() \n
		No command help available \n
			:return: multiplier: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:CLOCk:MULTiplier?')
		return Conversions.str_to_float(response)

	def set_multiplier(self, multiplier: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:CLOCk:MULTiplier \n
		Snippet: driver.source.bb.wlan.clock.set_multiplier(multiplier = 1.0) \n
		No command help available \n
			:param multiplier: No help available
		"""
		param = Conversions.decimal_value_to_str(multiplier)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:CLOCk:MULTiplier {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.ClockSourceB:
		"""SCPI: [SOURce<HW>]:BB:WLAN:CLOCk:SOURce \n
		Snippet: value: enums.ClockSourceB = driver.source.bb.wlan.clock.get_source() \n
		No command help available \n
			:return: source: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:CLOCk:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.ClockSourceB)

	def set_source(self, source: enums.ClockSourceB) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:CLOCk:SOURce \n
		Snippet: driver.source.bb.wlan.clock.set_source(source = enums.ClockSourceB.AINTernal) \n
		No command help available \n
			:param source: No help available
		"""
		param = Conversions.enum_scalar_to_str(source, enums.ClockSourceB)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:CLOCk:SOURce {param}')
