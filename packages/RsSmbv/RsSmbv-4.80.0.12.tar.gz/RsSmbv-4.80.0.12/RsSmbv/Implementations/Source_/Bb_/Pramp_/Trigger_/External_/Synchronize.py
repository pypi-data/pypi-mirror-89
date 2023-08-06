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
		"""SCPI: [SOURce<HW>]:BB:PRAMp:TRIGger:EXTernal:SYNChronize:OUTPut \n
		Snippet: value: bool = driver.source.bb.pramp.trigger.external.synchronize.get_output() \n
		No command help available \n
			:return: output: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:TRIGger:EXTernal:SYNChronize:OUTPut?')
		return Conversions.str_to_bool(response)

	def set_output(self, output: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:TRIGger:EXTernal:SYNChronize:OUTPut \n
		Snippet: driver.source.bb.pramp.trigger.external.synchronize.set_output(output = False) \n
		No command help available \n
			:param output: No help available
		"""
		param = Conversions.bool_to_str(output)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:TRIGger:EXTernal:SYNChronize:OUTPut {param}')
