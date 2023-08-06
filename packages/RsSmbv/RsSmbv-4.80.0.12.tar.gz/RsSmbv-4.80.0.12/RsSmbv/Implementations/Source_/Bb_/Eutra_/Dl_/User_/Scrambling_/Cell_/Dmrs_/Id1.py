from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Id1:
	"""Id1 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("id1", core, parent)

	def set(self, ident: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:SCRambling:CELL<ST>:DMRS:ID1 \n
		Snippet: driver.source.bb.eutra.dl.user.scrambling.cell.dmrs.id1.set(ident = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the DMRS scrambling identity. \n
			:param ident: integer Range: 0 to 503
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(ident)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:SCRambling:CELL{stream_cmd_val}:DMRS:ID1 {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:SCRambling:CELL<ST>:DMRS:ID1 \n
		Snippet: value: int = driver.source.bb.eutra.dl.user.scrambling.cell.dmrs.id1.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the DMRS scrambling identity. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: ident: integer Range: 0 to 503"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:SCRambling:CELL{stream_cmd_val}:DMRS:ID1?')
		return Conversions.str_to_int(response)
