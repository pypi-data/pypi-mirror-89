from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RmAttribute:
	"""RmAttribute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rmAttribute", core, parent)

	def set(self, rm_attribute: int, channel=repcap.Channel.Default, transportChannel=repcap.TransportChannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:CHANnel<CH>:DPCH:TCHannel<DI>:RMATtribute \n
		Snippet: driver.source.bb.w3Gpp.bstation.enhanced.channel.dpch.tchannel.rmAttribute.set(rm_attribute = 1, channel = repcap.Channel.Default, transportChannel = repcap.TransportChannel.Default) \n
		Sets data rate matching. \n
			:param rm_attribute: integer Range: 1 to 1024
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')"""
		param = Conversions.decimal_value_to_str(rm_attribute)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:DPCH:TCHannel{transportChannel_cmd_val}:RMATtribute {param}')

	def get(self, channel=repcap.Channel.Default, transportChannel=repcap.TransportChannel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:CHANnel<CH>:DPCH:TCHannel<DI>:RMATtribute \n
		Snippet: value: int = driver.source.bb.w3Gpp.bstation.enhanced.channel.dpch.tchannel.rmAttribute.get(channel = repcap.Channel.Default, transportChannel = repcap.TransportChannel.Default) \n
		Sets data rate matching. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')
			:return: rm_attribute: integer Range: 1 to 1024"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:DPCH:TCHannel{transportChannel_cmd_val}:RMATtribute?')
		return Conversions.str_to_int(response)
