from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sequence:
	"""Sequence commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sequence", core, parent)

	def get_increment(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:SCONtrol:SEQuence:INCRement \n
		Snippet: value: float = driver.source.bb.wlan.psdu.mac.scontrol.sequence.get_increment() \n
		No command help available \n
			:return: increment: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:SCONtrol:SEQuence:INCRement?')
		return Conversions.str_to_float(response)

	def set_increment(self, increment: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:SCONtrol:SEQuence:INCRement \n
		Snippet: driver.source.bb.wlan.psdu.mac.scontrol.sequence.set_increment(increment = 1.0) \n
		No command help available \n
			:param increment: No help available
		"""
		param = Conversions.decimal_value_to_str(increment)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:SCONtrol:SEQuence:INCRement {param}')

	def get_start(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:SCONtrol:SEQuence:STARt \n
		Snippet: value: List[str] = driver.source.bb.wlan.psdu.mac.scontrol.sequence.get_start() \n
		No command help available \n
			:return: start: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:SCONtrol:SEQuence:STARt?')
		return Conversions.str_to_str_list(response)

	def set_start(self, start: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:PSDU:MAC:SCONtrol:SEQuence:STARt \n
		Snippet: driver.source.bb.wlan.psdu.mac.scontrol.sequence.set_start(start = ['raw1', 'raw2', 'raw3']) \n
		No command help available \n
			:param start: No help available
		"""
		param = Conversions.list_to_csv_str(start)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:SCONtrol:SEQuence:STARt {param}')
