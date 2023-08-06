from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Foffset:
	"""Foffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("foffset", core, parent)

	def set(self, fall_offset: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TRIGger:OUTPut<CH>:FOFFset \n
		Snippet: driver.source.bb.eutra.trigger.output.foffset.set(fall_offset = 1, channel = repcap.Channel.Default) \n
		Sets the rise offset for on/off ratio marker in number of samples. \n
			:param fall_offset: integer Range: -640000 to 640000
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(fall_offset)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TRIGger:OUTPut{channel_cmd_val}:FOFFset {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TRIGger:OUTPut<CH>:FOFFset \n
		Snippet: value: int = driver.source.bb.eutra.trigger.output.foffset.get(channel = repcap.Channel.Default) \n
		Sets the rise offset for on/off ratio marker in number of samples. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: fall_offset: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:TRIGger:OUTPut{channel_cmd_val}:FOFFset?')
		return Conversions.str_to_int(response)
