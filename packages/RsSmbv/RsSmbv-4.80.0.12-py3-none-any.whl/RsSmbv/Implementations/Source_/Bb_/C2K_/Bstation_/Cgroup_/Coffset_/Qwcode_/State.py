from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, stream=repcap.Stream.Default, channelGroup=repcap.ChannelGroup.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI>:COFFset<CH>:QWCode:STATe \n
		Snippet: driver.source.bb.c2K.bstation.cgroup.coffset.qwcode.state.set(state = False, stream = repcap.Stream.Default, channelGroup = repcap.ChannelGroup.Default, channel = repcap.Channel.Default) \n
		Activates/deactivates the use of the quasi orthogonal Walsh codes for the channel. The quasi orthogonal Walsh Code set is
		selected for all channels of the base station with command method RsSmbv.Source.Bb.C2K.Bstation.Qwset.set.
		For the traffic channels, this value is specific for the selected radio configuration. It is only available for radio
		configuration 3 and higher. \n
			:param state: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelGroup: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coffset')"""
		param = Conversions.bool_to_str(state)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channelGroup_cmd_val = self._base.get_repcap_cmd_value(channelGroup, repcap.ChannelGroup)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:CGRoup{channelGroup_cmd_val}:COFFset{channel_cmd_val}:QWCode:STATe {param}')

	def get(self, stream=repcap.Stream.Default, channelGroup=repcap.ChannelGroup.Default, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI>:COFFset<CH>:QWCode:STATe \n
		Snippet: value: bool = driver.source.bb.c2K.bstation.cgroup.coffset.qwcode.state.get(stream = repcap.Stream.Default, channelGroup = repcap.ChannelGroup.Default, channel = repcap.Channel.Default) \n
		Activates/deactivates the use of the quasi orthogonal Walsh codes for the channel. The quasi orthogonal Walsh Code set is
		selected for all channels of the base station with command method RsSmbv.Source.Bb.C2K.Bstation.Qwset.set.
		For the traffic channels, this value is specific for the selected radio configuration. It is only available for radio
		configuration 3 and higher. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelGroup: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coffset')
			:return: state: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channelGroup_cmd_val = self._base.get_repcap_cmd_value(channelGroup, repcap.ChannelGroup)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:CGRoup{channelGroup_cmd_val}:COFFset{channel_cmd_val}:QWCode:STATe?')
		return Conversions.str_to_bool(response)
