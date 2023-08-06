from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sp15K:
	"""Sp15K commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sp15K", core, parent)

	def get_trtsamples(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:TDWind:SP15K:TRTSamples \n
		Snippet: value: int = driver.source.bb.nr5G.output.tdWind.sp15K.get_trtsamples() \n
		No command help available \n
			:return: transition_sampl: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:TDWind:SP15K:TRTSamples?')
		return Conversions.str_to_int(response)

	def get_tr_time(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:TDWind:SP15K:TRTime \n
		Snippet: value: float = driver.source.bb.nr5G.output.tdWind.sp15K.get_tr_time() \n
		No command help available \n
			:return: transition_time: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:TDWind:SP15K:TRTime?')
		return Conversions.str_to_float(response)

	def set_tr_time(self, transition_time: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:TDWind:SP15K:TRTime \n
		Snippet: driver.source.bb.nr5G.output.tdWind.sp15K.set_tr_time(transition_time = 1.0) \n
		No command help available \n
			:param transition_time: No help available
		"""
		param = Conversions.decimal_value_to_str(transition_time)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:TDWind:SP15K:TRTime {param}')
