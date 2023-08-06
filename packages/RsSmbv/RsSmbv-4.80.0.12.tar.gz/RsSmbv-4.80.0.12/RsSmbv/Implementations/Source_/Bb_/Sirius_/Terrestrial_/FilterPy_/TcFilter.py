from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TcFilter:
	"""TcFilter commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tcFilter", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:SIRius:TERRestrial:FILTer:TCFilter:[STATe] \n
		Snippet: value: bool = driver.source.bb.sirius.terrestrial.filterPy.tcFilter.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:SIRius:TERRestrial:FILTer:TCFilter:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:SIRius:TERRestrial:FILTer:TCFilter:[STATe] \n
		Snippet: driver.source.bb.sirius.terrestrial.filterPy.tcFilter.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:SIRius:TERRestrial:FILTer:TCFilter:STATe {param}')
