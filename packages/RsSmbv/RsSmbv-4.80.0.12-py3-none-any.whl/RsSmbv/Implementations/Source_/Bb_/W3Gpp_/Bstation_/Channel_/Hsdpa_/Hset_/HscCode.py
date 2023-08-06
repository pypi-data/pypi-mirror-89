from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HscCode:
	"""HscCode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hscCode", core, parent)

	def set(self, hsc_code: float, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:HSCCode \n
		Snippet: driver.source.bb.w3Gpp.bstation.channel.hsdpa.hset.hscCode.set(hsc_code = 1.0, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the channelization code of the HS-SCCH. \n
			:param hsc_code: float Range: 0 to 127
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.decimal_value_to_str(hsc_code)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:HSCCode {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:HSCCode \n
		Snippet: value: float = driver.source.bb.w3Gpp.bstation.channel.hsdpa.hset.hscCode.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the channelization code of the HS-SCCH. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: hsc_code: float Range: 0 to 127"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:HSCCode?')
		return Conversions.str_to_float(response)
