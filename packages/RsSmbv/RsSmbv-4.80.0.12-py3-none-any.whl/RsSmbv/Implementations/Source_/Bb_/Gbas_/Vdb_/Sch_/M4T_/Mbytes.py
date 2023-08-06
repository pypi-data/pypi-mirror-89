from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mbytes:
	"""Mbytes commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mbytes", core, parent)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:SCH:M4T<ST>:MBYTes \n
		Snippet: value: int = driver.source.bb.gbas.vdb.sch.m4T.mbytes.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the total number of bytes per message type. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'M4T')
			:return: bytes: integer Range: 0 to 5000"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:SCH:M4T{stream_cmd_val}:MBYTes?')
		return Conversions.str_to_int(response)
