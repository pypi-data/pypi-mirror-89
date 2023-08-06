from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.Utilities import trim_str_response
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dselect:
	"""Dselect commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dselect", core, parent)

	def set(self, dselect: str, stream=repcap.Stream.Default, channelGroup=repcap.ChannelGroup.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI>:COFFset<CH>:TPC:DATA:DSELect \n
		Snippet: driver.source.bb.c2K.bstation.cgroup.coffset.tpc.data.dselect.set(dselect = '1', stream = repcap.Stream.Default, channelGroup = repcap.ChannelGroup.Default, channel = repcap.Channel.Default) \n
		The command selects the data list for the DLISt data source selection. Power control is available for sub channel types
		F-DCCH and F-FCH. F-DCCH is only generated for radio configurations 3, 4 and 5. The lists are stored as files with the
		fixed file extensions *.dm_iqd in a directory of the user's choice. The directory applicable to the following commands is
		defined with the command method RsSmbv.MassMemory.currentDirectory. To access the files in this directory, you only have
		to give the file name, without the path and the file extension. For the traffic channels, this value is specific for the
		selected radio configuration. \n
			:param dselect: string
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelGroup: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coffset')"""
		param = Conversions.value_to_quoted_str(dselect)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channelGroup_cmd_val = self._base.get_repcap_cmd_value(channelGroup, repcap.ChannelGroup)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:CGRoup{channelGroup_cmd_val}:COFFset{channel_cmd_val}:TPC:DATA:DSELect {param}')

	def get(self, stream=repcap.Stream.Default, channelGroup=repcap.ChannelGroup.Default, channel=repcap.Channel.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:C2K:BSTation<ST>:CGRoup<DI>:COFFset<CH>:TPC:DATA:DSELect \n
		Snippet: value: str = driver.source.bb.c2K.bstation.cgroup.coffset.tpc.data.dselect.get(stream = repcap.Stream.Default, channelGroup = repcap.ChannelGroup.Default, channel = repcap.Channel.Default) \n
		The command selects the data list for the DLISt data source selection. Power control is available for sub channel types
		F-DCCH and F-FCH. F-DCCH is only generated for radio configurations 3, 4 and 5. The lists are stored as files with the
		fixed file extensions *.dm_iqd in a directory of the user's choice. The directory applicable to the following commands is
		defined with the command method RsSmbv.MassMemory.currentDirectory. To access the files in this directory, you only have
		to give the file name, without the path and the file extension. For the traffic channels, this value is specific for the
		selected radio configuration. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelGroup: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cgroup')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coffset')
			:return: dselect: string"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channelGroup_cmd_val = self._base.get_repcap_cmd_value(channelGroup, repcap.ChannelGroup)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:CGRoup{channelGroup_cmd_val}:COFFset{channel_cmd_val}:TPC:DATA:DSELect?')
		return trim_str_response(response)
