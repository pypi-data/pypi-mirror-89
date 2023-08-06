from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Clipping:
	"""Clipping commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("clipping", core, parent)

	def get_level(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NFC:CLIPping:LEVel \n
		Snippet: value: int = driver.source.bb.nfc.clipping.get_level() \n
		Sets the limit for clipping. \n
			:return: level: integer Range: 1 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:CLIPping:LEVel?')
		return Conversions.str_to_int(response)

	def set_level(self, level: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CLIPping:LEVel \n
		Snippet: driver.source.bb.nfc.clipping.set_level(level = 1) \n
		Sets the limit for clipping. \n
			:param level: integer Range: 1 to 100
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CLIPping:LEVel {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ClipMode:
		"""SCPI: [SOURce<HW>]:BB:NFC:CLIPping:MODE \n
		Snippet: value: enums.ClipMode = driver.source.bb.nfc.clipping.get_mode() \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:CLIPping:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ClipMode)

	def set_mode(self, mode: enums.ClipMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CLIPping:MODE \n
		Snippet: driver.source.bb.nfc.clipping.set_mode(mode = enums.ClipMode.SCALar) \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ClipMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CLIPping:MODE {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NFC:CLIPping:STATe \n
		Snippet: value: bool = driver.source.bb.nfc.clipping.get_state() \n
		Switches baseband clipping on and off. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:CLIPping:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CLIPping:STATe \n
		Snippet: driver.source.bb.nfc.clipping.set_state(state = False) \n
		Switches baseband clipping on and off. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CLIPping:STATe {param}')
