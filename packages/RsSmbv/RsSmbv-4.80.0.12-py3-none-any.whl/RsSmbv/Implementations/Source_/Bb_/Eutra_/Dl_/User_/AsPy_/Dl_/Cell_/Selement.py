from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Selement:
	"""Selement commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("selement", core, parent)

	def set(self, sel_elem: int, channel=repcap.Channel.Default, stream=repcap.Stream.Nr1) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST>:SELement \n
		Snippet: driver.source.bb.eutra.dl.user.asPy.dl.cell.selement.set(sel_elem = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Nr1) \n
		Selects a table element (i.e. table row) . \n
			:param sel_elem: integer Range: 0 to 1499
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1"""
		param = Conversions.decimal_value_to_str(sel_elem)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{stream_cmd_val}:SELement {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Nr1) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST>:SELement \n
		Snippet: value: int = driver.source.bb.eutra.dl.user.asPy.dl.cell.selement.get(channel = repcap.Channel.Default, stream = repcap.Stream.Nr1) \n
		Selects a table element (i.e. table row) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1
			:return: sel_elem: integer Range: 0 to 1499"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{stream_cmd_val}:SELement?')
		return Conversions.str_to_int(response)
