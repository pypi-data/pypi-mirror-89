from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Reference:
	"""Reference commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("reference", core, parent)

	def set(self, reference: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:TBS:REFerence \n
		Snippet: driver.source.bb.w3Gpp.bstation.channel.hsdpa.hset.tbs.reference.set(reference = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		While working in less operation mode, this command is signaled instead of the command method RsSmbv.Source.Bb.W3Gpp.
		Bstation.Channel.Hsdpa.Hset.Tbs.Index.set. \n
			:param reference: integer Range: 0 to 3
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.decimal_value_to_str(reference)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:TBS:REFerence {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:TBS:REFerence \n
		Snippet: value: int = driver.source.bb.w3Gpp.bstation.channel.hsdpa.hset.tbs.reference.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		While working in less operation mode, this command is signaled instead of the command method RsSmbv.Source.Bb.W3Gpp.
		Bstation.Channel.Hsdpa.Hset.Tbs.Index.set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: reference: integer Range: 0 to 3"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:TBS:REFerence?')
		return Conversions.str_to_int(response)
