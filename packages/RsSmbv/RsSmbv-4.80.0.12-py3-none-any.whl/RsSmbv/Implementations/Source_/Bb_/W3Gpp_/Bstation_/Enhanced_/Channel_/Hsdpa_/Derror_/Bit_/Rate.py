from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rate:
	"""Rate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rate", core, parent)

	def set(self, rate: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:[ENHanced]:CHANnel<CH>:HSDPa:DERRor:BIT:RATE \n
		Snippet: driver.source.bb.w3Gpp.bstation.enhanced.channel.hsdpa.derror.bit.rate.set(rate = 1.0, channel = repcap.Channel.Default) \n
		Sets the bit error rate. \n
			:param rate: float
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.decimal_value_to_str(rate)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:HSDPa:DERRor:BIT:RATE {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:[ENHanced]:CHANnel<CH>:HSDPa:DERRor:BIT:RATE \n
		Snippet: value: float = driver.source.bb.w3Gpp.bstation.enhanced.channel.hsdpa.derror.bit.rate.get(channel = repcap.Channel.Default) \n
		Sets the bit error rate. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: rate: float"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:HSDPa:DERRor:BIT:RATE?')
		return Conversions.str_to_float(response)
