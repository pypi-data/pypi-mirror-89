from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Synchronize:
	"""Synchronize commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("synchronize", core, parent)

	def get_output(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TRIGger:EXTernal:SYNChronize:OUTPut \n
		Snippet: value: bool = driver.source.bb.evdo.trigger.external.synchronize.get_output() \n
		Enables signal output synchronous to the trigger event. \n
			:return: output: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:TRIGger:EXTernal:SYNChronize:OUTPut?')
		return Conversions.str_to_bool(response)

	def set_output(self, output: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TRIGger:EXTernal:SYNChronize:OUTPut \n
		Snippet: driver.source.bb.evdo.trigger.external.synchronize.set_output(output = False) \n
		Enables signal output synchronous to the trigger event. \n
			:param output: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(output)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TRIGger:EXTernal:SYNChronize:OUTPut {param}')
