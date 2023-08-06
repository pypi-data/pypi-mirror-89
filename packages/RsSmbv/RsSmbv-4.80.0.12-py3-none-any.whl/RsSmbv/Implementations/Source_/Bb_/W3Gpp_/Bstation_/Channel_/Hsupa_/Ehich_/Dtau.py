from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dtau:
	"""Dtau commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dtau", core, parent)

	def set(self, dtau: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:[HSUPa]:EHICh:DTAU \n
		Snippet: driver.source.bb.w3Gpp.bstation.channel.hsupa.ehich.dtau.set(dtau = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the offset of the downlink dedicated offset channels. \n
			:param dtau: integer Range: 0 to 149
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.decimal_value_to_str(dtau)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSUPa:EHICh:DTAU {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:[HSUPa]:EHICh:DTAU \n
		Snippet: value: int = driver.source.bb.w3Gpp.bstation.channel.hsupa.ehich.dtau.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the offset of the downlink dedicated offset channels. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: dtau: integer Range: 0 to 149"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSUPa:EHICh:DTAU?')
		return Conversions.str_to_int(response)
