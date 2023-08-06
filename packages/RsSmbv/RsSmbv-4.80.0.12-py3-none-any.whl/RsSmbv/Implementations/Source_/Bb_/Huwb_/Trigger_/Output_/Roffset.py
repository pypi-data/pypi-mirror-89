from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Roffset:
	"""Roffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("roffset", core, parent)

	def set(self, mark_rise_offs: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:TRIGger:OUTPut<CH>:ROFFset \n
		Snippet: driver.source.bb.huwb.trigger.output.roffset.set(mark_rise_offs = 1, channel = repcap.Channel.Default) \n
		Sets the rise/fall offset. \n
			:param mark_rise_offs: integer Range: -640000 to 640000
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(mark_rise_offs)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:TRIGger:OUTPut{channel_cmd_val}:ROFFset {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:HUWB:TRIGger:OUTPut<CH>:ROFFset \n
		Snippet: value: int = driver.source.bb.huwb.trigger.output.roffset.get(channel = repcap.Channel.Default) \n
		Sets the rise/fall offset. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: mark_rise_offs: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:HUWB:TRIGger:OUTPut{channel_cmd_val}:ROFFset?')
		return Conversions.str_to_int(response)
