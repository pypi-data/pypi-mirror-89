from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Asetting:
	"""Asetting commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("asetting", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BBIN:DIGital:ASETting:STATe \n
		Snippet: value: bool = driver.source.bbin.digital.asetting.get_state() \n
		Activates automatic adjustment of the baseband input signal. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:DIGital:ASETting:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:DIGital:ASETting:STATe \n
		Snippet: driver.source.bbin.digital.asetting.set_state(state = False) \n
		Activates automatic adjustment of the baseband input signal. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:DIGital:ASETting:STATe {param}')
