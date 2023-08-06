from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Slfmt:
	"""Slfmt commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("slfmt", core, parent)

	def set(self, spec_slot_fmt_idx: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TRIGger:OUTPut<CH>:SSC:SLFMt \n
		Snippet: driver.source.bb.nr5G.trigger.output.ssc.slfmt.set(spec_slot_fmt_idx = 1, channel = repcap.Channel.Default) \n
		Sets the special slot format index of the special slot included in a UL/DL pattern containing a marker according to . \n
			:param spec_slot_fmt_idx: integer Range: 0 to 45
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(spec_slot_fmt_idx)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TRIGger:OUTPut{channel_cmd_val}:SSC:SLFMt {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TRIGger:OUTPut<CH>:SSC:SLFMt \n
		Snippet: value: int = driver.source.bb.nr5G.trigger.output.ssc.slfmt.get(channel = repcap.Channel.Default) \n
		Sets the special slot format index of the special slot included in a UL/DL pattern containing a marker according to . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: spec_slot_fmt_idx: integer Range: 0 to 45"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:TRIGger:OUTPut{channel_cmd_val}:SSC:SLFMt?')
		return Conversions.str_to_int(response)
