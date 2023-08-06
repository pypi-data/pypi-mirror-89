from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SubChannel:
	"""SubChannel commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("subChannel", core, parent)

	def set(self, subchannel: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:SCI<CH>:SUBChannel \n
		Snippet: driver.source.bb.eutra.ul.ue.sl.sci.subChannel.set(subchannel = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the used subchannel. \n
			:param subchannel: integer Range: 0 to 19
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sci')"""
		param = Conversions.decimal_value_to_str(subchannel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:SCI{channel_cmd_val}:SUBChannel {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:SCI<CH>:SUBChannel \n
		Snippet: value: int = driver.source.bb.eutra.ul.ue.sl.sci.subChannel.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the used subchannel. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sci')
			:return: subchannel: integer Range: 0 to 19"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:SCI{channel_cmd_val}:SUBChannel?')
		return Conversions.str_to_int(response)
