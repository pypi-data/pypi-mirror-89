from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SyOffset:
	"""SyOffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("syOffset", core, parent)

	def set(self, prs_res_symb_off: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default, srsRsrcSetRsrc=repcap.SrsRsrcSetRsrc.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:RSET<ST>:RES<DIR>:SYOFfset \n
		Snippet: driver.source.bb.nr5G.node.cell.prs.rset.res.syOffset.set(prs_res_symb_off = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default, srsRsrcSetRsrc = repcap.SrsRsrcSetRsrc.Default) \n
		Sets the starting symbol of the resource within a slot. \n
			:param prs_res_symb_off: integer Range: 0 to 12
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rset')
			:param srsRsrcSetRsrc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')"""
		param = Conversions.decimal_value_to_str(prs_res_symb_off)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		srsRsrcSetRsrc_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSetRsrc, repcap.SrsRsrcSetRsrc)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:RSET{stream_cmd_val}:RES{srsRsrcSetRsrc_cmd_val}:SYOFfset {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, srsRsrcSetRsrc=repcap.SrsRsrcSetRsrc.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:RSET<ST>:RES<DIR>:SYOFfset \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.prs.rset.res.syOffset.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, srsRsrcSetRsrc = repcap.SrsRsrcSetRsrc.Default) \n
		Sets the starting symbol of the resource within a slot. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rset')
			:param srsRsrcSetRsrc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')
			:return: prs_res_symb_off: integer Range: 0 to 12"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		srsRsrcSetRsrc_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSetRsrc, repcap.SrsRsrcSetRsrc)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:RSET{stream_cmd_val}:RES{srsRsrcSetRsrc_cmd_val}:SYOFfset?')
		return Conversions.str_to_int(response)
