from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Waveform:
	"""Waveform commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("waveform", core, parent)

	def set_create(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:WAVeform:CREate \n
		Snippet: driver.source.bb.pramp.waveform.set_create(filename = '1') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:WAVeform:CREate {param}')
