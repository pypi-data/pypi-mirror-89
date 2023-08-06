from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Imaginary:
	"""Imaginary commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("imaginary", core, parent)

	def set(self, prs_ap_imag: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default, srsRsrcSetRsrc=repcap.SrsRsrcSetRsrc.Default, column=repcap.Column.Default, row=repcap.Row.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:RSET<ST>:RES<DIR>:APMap:COL<GR>:ROW<USER>:IMAGinary \n
		Snippet: driver.source.bb.nr5G.node.cell.prs.rset.res.apMap.col.row.imaginary.set(prs_ap_imag = 1.0, channel = repcap.Channel.Default, stream = repcap.Stream.Default, srsRsrcSetRsrc = repcap.SrsRsrcSetRsrc.Default, column = repcap.Column.Default, row = repcap.Row.Default) \n
		Sets the mapping of the antenna ports (AP) for the PRS resource, if Cartesian coordinates are used. \n
			:param prs_ap_imag: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rset')
			:param srsRsrcSetRsrc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')
			:param column: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Col')
			:param row: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')"""
		param = Conversions.decimal_value_to_str(prs_ap_imag)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		srsRsrcSetRsrc_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSetRsrc, repcap.SrsRsrcSetRsrc)
		column_cmd_val = self._base.get_repcap_cmd_value(column, repcap.Column)
		row_cmd_val = self._base.get_repcap_cmd_value(row, repcap.Row)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:RSET{stream_cmd_val}:RES{srsRsrcSetRsrc_cmd_val}:APMap:COL{column_cmd_val}:ROW{row_cmd_val}:IMAGinary {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, srsRsrcSetRsrc=repcap.SrsRsrcSetRsrc.Default, column=repcap.Column.Default, row=repcap.Row.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:RSET<ST>:RES<DIR>:APMap:COL<GR>:ROW<USER>:IMAGinary \n
		Snippet: value: float = driver.source.bb.nr5G.node.cell.prs.rset.res.apMap.col.row.imaginary.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, srsRsrcSetRsrc = repcap.SrsRsrcSetRsrc.Default, column = repcap.Column.Default, row = repcap.Row.Default) \n
		Sets the mapping of the antenna ports (AP) for the PRS resource, if Cartesian coordinates are used. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rset')
			:param srsRsrcSetRsrc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')
			:param column: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Col')
			:param row: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')
			:return: prs_ap_imag: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		srsRsrcSetRsrc_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSetRsrc, repcap.SrsRsrcSetRsrc)
		column_cmd_val = self._base.get_repcap_cmd_value(column, repcap.Column)
		row_cmd_val = self._base.get_repcap_cmd_value(row, repcap.Row)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:RSET{stream_cmd_val}:RES{srsRsrcSetRsrc_cmd_val}:APMap:COL{column_cmd_val}:ROW{row_cmd_val}:IMAGinary?')
		return Conversions.str_to_float(response)
