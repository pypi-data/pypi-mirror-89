from ...............Internal.Core import Core
from ...............Internal.CommandsGroup import CommandsGroup
from ...............Internal import Conversions
from ............... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CycShift:
	"""CycShift commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cycShift", core, parent)

	def set(self, srs_rs_cyclic_shif: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, srsRsrcSet=repcap.SrsRsrcSet.Default, srsRsrcSetRsrc=repcap.SrsRsrcSetRsrc.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:SRS:RS:SET<GR>:RES<USER>:SEQ:CYCShift \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.ul.bwp.srs.rs.set.res.seq.cycShift.set(srs_rs_cyclic_shif = 1.0, channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default, srsRsrcSet = repcap.SrsRsrcSet.Default, srsRsrcSetRsrc = repcap.SrsRsrcSetRsrc.Default) \n
		Sets the number of cyclic shifts, required for the SRS sequence generation. \n
			:param srs_rs_cyclic_shif: float Range: 0 to 11
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param srsRsrcSet: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Set')
			:param srsRsrcSetRsrc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')"""
		param = Conversions.decimal_value_to_str(srs_rs_cyclic_shif)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		srsRsrcSet_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSet, repcap.SrsRsrcSet)
		srsRsrcSetRsrc_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSetRsrc, repcap.SrsRsrcSetRsrc)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:SRS:RS:SET{srsRsrcSet_cmd_val}:RES{srsRsrcSetRsrc_cmd_val}:SEQ:CYCShift {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, srsRsrcSet=repcap.SrsRsrcSet.Default, srsRsrcSetRsrc=repcap.SrsRsrcSetRsrc.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:SRS:RS:SET<GR>:RES<USER>:SEQ:CYCShift \n
		Snippet: value: float = driver.source.bb.nr5G.ubwp.user.cell.ul.bwp.srs.rs.set.res.seq.cycShift.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default, srsRsrcSet = repcap.SrsRsrcSet.Default, srsRsrcSetRsrc = repcap.SrsRsrcSetRsrc.Default) \n
		Sets the number of cyclic shifts, required for the SRS sequence generation. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param srsRsrcSet: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Set')
			:param srsRsrcSetRsrc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')
			:return: srs_rs_cyclic_shif: float Range: 0 to 11"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		srsRsrcSet_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSet, repcap.SrsRsrcSet)
		srsRsrcSetRsrc_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSetRsrc, repcap.SrsRsrcSetRsrc)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:SRS:RS:SET{srsRsrcSet_cmd_val}:RES{srsRsrcSetRsrc_cmd_val}:SEQ:CYCShift?')
		return Conversions.str_to_float(response)
