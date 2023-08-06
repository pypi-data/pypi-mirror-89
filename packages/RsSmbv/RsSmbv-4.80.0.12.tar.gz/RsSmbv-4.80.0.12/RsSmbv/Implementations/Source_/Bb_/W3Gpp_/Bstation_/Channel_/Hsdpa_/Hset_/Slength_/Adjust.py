from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Adjust:
	"""Adjust commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("adjust", core, parent)

	def set(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:SLENgth:ADJust \n
		Snippet: driver.source.bb.w3Gpp.bstation.channel.hsdpa.hset.slength.adjust.set(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the ARB sequence length to the suggested value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:SLENgth:ADJust')

	def set_with_opc(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:SLENgth:ADJust \n
		Snippet: driver.source.bb.w3Gpp.bstation.channel.hsdpa.hset.slength.adjust.set_with_opc(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the ARB sequence length to the suggested value. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:SLENgth:ADJust')
