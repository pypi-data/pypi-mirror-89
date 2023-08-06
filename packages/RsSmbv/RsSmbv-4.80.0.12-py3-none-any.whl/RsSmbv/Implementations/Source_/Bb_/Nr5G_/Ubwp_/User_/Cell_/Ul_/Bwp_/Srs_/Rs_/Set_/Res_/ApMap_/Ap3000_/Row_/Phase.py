from .................Internal.Core import Core
from .................Internal.CommandsGroup import CommandsGroup
from .................Internal import Conversions
from ................. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Phase:
	"""Phase commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("phase", core, parent)

	def set(self, srs_ap_map_data_pha: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, srsRsrcSet=repcap.SrsRsrcSet.Default, srsRsrcSetRsrc=repcap.SrsRsrcSetRsrc.Default, row=repcap.Row.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:SRS:RS:SET<GR>:RES<USER>:APMap:AP3000:ROW<S3US>:PHASe \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.ul.bwp.srs.rs.set.res.apMap.ap3000.row.phase.set(srs_ap_map_data_pha = 1.0, channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default, srsRsrcSet = repcap.SrsRsrcSet.Default, srsRsrcSetRsrc = repcap.SrsRsrcSetRsrc.Default, row = repcap.Row.Default) \n
		No command help available \n
			:param srs_ap_map_data_pha: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param srsRsrcSet: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Set')
			:param srsRsrcSetRsrc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')
			:param row: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')"""
		param = Conversions.decimal_value_to_str(srs_ap_map_data_pha)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		srsRsrcSet_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSet, repcap.SrsRsrcSet)
		srsRsrcSetRsrc_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSetRsrc, repcap.SrsRsrcSetRsrc)
		row_cmd_val = self._base.get_repcap_cmd_value(row, repcap.Row)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:SRS:RS:SET{srsRsrcSet_cmd_val}:RES{srsRsrcSetRsrc_cmd_val}:APMap:AP3000:ROW{row_cmd_val}:PHASe {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, srsRsrcSet=repcap.SrsRsrcSet.Default, srsRsrcSetRsrc=repcap.SrsRsrcSetRsrc.Default, row=repcap.Row.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:SRS:RS:SET<GR>:RES<USER>:APMap:AP3000:ROW<S3US>:PHASe \n
		Snippet: value: float = driver.source.bb.nr5G.ubwp.user.cell.ul.bwp.srs.rs.set.res.apMap.ap3000.row.phase.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default, srsRsrcSet = repcap.SrsRsrcSet.Default, srsRsrcSetRsrc = repcap.SrsRsrcSetRsrc.Default, row = repcap.Row.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param srsRsrcSet: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Set')
			:param srsRsrcSetRsrc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')
			:param row: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')
			:return: srs_ap_map_data_pha: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		srsRsrcSet_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSet, repcap.SrsRsrcSet)
		srsRsrcSetRsrc_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSetRsrc, repcap.SrsRsrcSetRsrc)
		row_cmd_val = self._base.get_repcap_cmd_value(row, repcap.Row)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:SRS:RS:SET{srsRsrcSet_cmd_val}:RES{srsRsrcSetRsrc_cmd_val}:APMap:AP3000:ROW{row_cmd_val}:PHASe?')
		return Conversions.str_to_float(response)
