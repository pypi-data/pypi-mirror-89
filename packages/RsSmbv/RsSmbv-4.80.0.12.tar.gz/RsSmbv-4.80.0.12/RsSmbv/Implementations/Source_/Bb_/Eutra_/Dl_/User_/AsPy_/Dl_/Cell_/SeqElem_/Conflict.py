from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Conflict:
	"""Conflict commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("conflict", core, parent)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Nr1) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST>:SEQelem:CONFlict \n
		Snippet: value: bool = driver.source.bb.eutra.dl.user.asPy.dl.cell.seqElem.conflict.get(channel = repcap.Channel.Default, stream = repcap.Stream.Nr1) \n
		Queries if there is conflict. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1
			:return: dla_seq_conflict: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{stream_cmd_val}:SEQelem:CONFlict?')
		return Conversions.str_to_bool(response)
