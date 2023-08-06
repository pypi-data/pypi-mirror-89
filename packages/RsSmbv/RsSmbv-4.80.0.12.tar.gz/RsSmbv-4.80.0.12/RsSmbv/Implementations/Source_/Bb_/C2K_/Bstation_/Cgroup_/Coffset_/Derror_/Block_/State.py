from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, stream=repcap.Stream.Default, channelGroup=repcap.ChannelGroup.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI>:COFFset<CH>:DERRor:BLOCk:STATe \n
		Snippet: driver.source.bb.c2K.bstation.cgroup.coffset.derror.block.state.set(state = False, stream = repcap.Stream.Default, channelGroup = repcap.ChannelGroup.Default, channel = repcap.Channel.Default) \n
		No command help available \n
			:param state: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelGroup: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coffset')"""
		param = Conversions.bool_to_str(state)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channelGroup_cmd_val = self._base.get_repcap_cmd_value(channelGroup, repcap.ChannelGroup)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:CGRoup{channelGroup_cmd_val}:COFFset{channel_cmd_val}:DERRor:BLOCk:STATe {param}')

	def get(self, stream=repcap.Stream.Default, channelGroup=repcap.ChannelGroup.Default, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI>:COFFset<CH>:DERRor:BLOCk:STATe \n
		Snippet: value: bool = driver.source.bb.c2K.bstation.cgroup.coffset.derror.block.state.get(stream = repcap.Stream.Default, channelGroup = repcap.ChannelGroup.Default, channel = repcap.Channel.Default) \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelGroup: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coffset')
			:return: state: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channelGroup_cmd_val = self._base.get_repcap_cmd_value(channelGroup, repcap.ChannelGroup)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:CGRoup{channelGroup_cmd_val}:COFFset{channel_cmd_val}:DERRor:BLOCk:STATe?')
		return Conversions.str_to_bool(response)
