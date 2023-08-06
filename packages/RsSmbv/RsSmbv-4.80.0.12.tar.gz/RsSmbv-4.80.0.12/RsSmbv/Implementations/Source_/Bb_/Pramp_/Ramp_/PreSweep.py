from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PreSweep:
	"""PreSweep commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("preSweep", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:PRESweep:STATe \n
		Snippet: value: bool = driver.source.bb.pramp.ramp.preSweep.get_state() \n
		No command help available \n
			:return: enable_pre_sweep: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:PRESweep:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, enable_pre_sweep: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:PRESweep:STATe \n
		Snippet: driver.source.bb.pramp.ramp.preSweep.set_state(enable_pre_sweep = False) \n
		No command help available \n
			:param enable_pre_sweep: No help available
		"""
		param = Conversions.bool_to_str(enable_pre_sweep)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:RAMP:PRESweep:STATe {param}')

	def get_time(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:PRESweep:TIME \n
		Snippet: value: float = driver.source.bb.pramp.ramp.preSweep.get_time() \n
		No command help available \n
			:return: pre_sweep_time: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:PRESweep:TIME?')
		return Conversions.str_to_float(response)

	def set_time(self, pre_sweep_time: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:PRESweep:TIME \n
		Snippet: driver.source.bb.pramp.ramp.preSweep.set_time(pre_sweep_time = 1.0) \n
		No command help available \n
			:param pre_sweep_time: No help available
		"""
		param = Conversions.decimal_value_to_str(pre_sweep_time)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:RAMP:PRESweep:TIME {param}')

	def get_level(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:PRESweep:[LEVel] \n
		Snippet: value: float = driver.source.bb.pramp.ramp.preSweep.get_level() \n
		No command help available \n
			:return: presweep_level: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:PRESweep:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, presweep_level: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:PRESweep:[LEVel] \n
		Snippet: driver.source.bb.pramp.ramp.preSweep.set_level(presweep_level = 1.0) \n
		No command help available \n
			:param presweep_level: No help available
		"""
		param = Conversions.decimal_value_to_str(presweep_level)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:RAMP:PRESweep:LEVel {param}')
