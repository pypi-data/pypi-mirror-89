from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RvState:
	"""RvState commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rvState", core, parent)

	def set(self, rv_state: bool, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:RVSTate \n
		Snippet: driver.source.bb.w3Gpp.bstation.channel.hsdpa.hset.rvState.set(rv_state = False, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Enables/disables the random variation of the modulation and number of codes (see 'Randomly Varying Modulation and Number
		of Codes (Type 3i) Settings') . \n
			:param rv_state: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.bool_to_str(rv_state)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:RVSTate {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:RVSTate \n
		Snippet: value: bool = driver.source.bb.w3Gpp.bstation.channel.hsdpa.hset.rvState.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Enables/disables the random variation of the modulation and number of codes (see 'Randomly Varying Modulation and Number
		of Codes (Type 3i) Settings') . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: rv_state: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:RVSTate?')
		return Conversions.str_to_bool(response)
