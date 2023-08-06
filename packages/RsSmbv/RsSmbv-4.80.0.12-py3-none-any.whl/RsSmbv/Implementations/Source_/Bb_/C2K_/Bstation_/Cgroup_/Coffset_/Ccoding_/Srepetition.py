from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Srepetition:
	"""Srepetition commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("srepetition", core, parent)

	def get(self, stream=repcap.Stream.Default, channelGroup=repcap.ChannelGroup.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI>:COFFset<CH>:CCODing:SREPetition \n
		Snippet: value: int = driver.source.bb.c2K.bstation.cgroup.coffset.ccoding.srepetition.get(stream = repcap.Stream.Default, channelGroup = repcap.ChannelGroup.Default, channel = repcap.Channel.Default) \n
		Queries symbol repetition rate. This value is only available for channel coding modes 'Complete' and 'Without
		Interleaving' (SOURce:BB:C2K:BST<n>:CGRoup<n>:COFFset<n>:CCODing:MODE COMP | NOIN) . For the traffic channels, this value
		is specific for the selected radio configuration. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelGroup: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coffset')
			:return: srrpetition: integer Range: 1 to 16"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channelGroup_cmd_val = self._base.get_repcap_cmd_value(channelGroup, repcap.ChannelGroup)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:CGRoup{channelGroup_cmd_val}:COFFset{channel_cmd_val}:CCODing:SREPetition?')
		return Conversions.str_to_int(response)
