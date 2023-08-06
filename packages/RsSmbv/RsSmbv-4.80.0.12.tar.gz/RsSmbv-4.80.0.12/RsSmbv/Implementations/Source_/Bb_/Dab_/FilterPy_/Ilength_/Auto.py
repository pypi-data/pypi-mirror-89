from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Auto:
	"""Auto commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("auto", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:DAB:FILTer:ILENgth:AUTO:[STATe] \n
		Snippet: value: bool = driver.source.bb.dab.filterPy.ilength.auto.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DAB:FILTer:ILENgth:AUTO:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:DAB:FILTer:ILENgth:AUTO:[STATe] \n
		Snippet: driver.source.bb.dab.filterPy.ilength.auto.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:FILTer:ILENgth:AUTO:STATe {param}')
