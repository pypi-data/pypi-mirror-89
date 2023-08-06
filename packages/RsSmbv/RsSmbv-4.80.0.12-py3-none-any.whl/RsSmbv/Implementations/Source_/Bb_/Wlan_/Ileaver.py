from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ileaver:
	"""Ileaver commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ileaver", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAN:ILEaver:STATe \n
		Snippet: value: bool = driver.source.bb.wlan.ileaver.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:ILEaver:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:ILEaver:STATe \n
		Snippet: driver.source.bb.wlan.ileaver.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:ILEaver:STATe {param}')
