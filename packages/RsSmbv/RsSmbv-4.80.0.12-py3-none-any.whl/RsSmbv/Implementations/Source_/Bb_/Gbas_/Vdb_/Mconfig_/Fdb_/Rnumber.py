from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rnumber:
	"""Rnumber commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rnumber", core, parent)

	def set(self, rnum: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:FDB<ST>:RNUMber \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.fdb.rnumber.set(rnum = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the runway number. \n
			:param rnum: integer Range: 1 to 36
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fdb')"""
		param = Conversions.decimal_value_to_str(rnum)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:FDB{stream_cmd_val}:RNUMber {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:FDB<ST>:RNUMber \n
		Snippet: value: int = driver.source.bb.gbas.vdb.mconfig.fdb.rnumber.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the runway number. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fdb')
			:return: rnum: integer Range: 1 to 36"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:FDB{stream_cmd_val}:RNUMber?')
		return Conversions.str_to_int(response)
