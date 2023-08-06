from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rframe:
	"""Rframe commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rframe", core, parent)

	def set(self, rep_frame: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:SCH:M2T<ST>:RFRame \n
		Snippet: driver.source.bb.gbas.vdb.sch.m2T.rframe.set(rep_frame = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the repetition rate for the respective message type. \n
			:param rep_frame: integer Range: 1 to 20
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'M2T')"""
		param = Conversions.decimal_value_to_str(rep_frame)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:SCH:M2T{stream_cmd_val}:RFRame {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:SCH:M2T<ST>:RFRame \n
		Snippet: value: int = driver.source.bb.gbas.vdb.sch.m2T.rframe.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the repetition rate for the respective message type. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'M2T')
			:return: rep_frame: integer Range: 1 to 20"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:SCH:M2T{stream_cmd_val}:RFRame?')
		return Conversions.str_to_int(response)
