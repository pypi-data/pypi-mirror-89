from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import enums
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RsType:
	"""RsType commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rsType", core, parent)

	def set(self, srs_rs_set_rs_type: enums.SrsRsSetRsTypeAll, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, srsRsrcSet=repcap.SrsRsrcSet.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:SRS:RS:SET<GR>:RSTYpe \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.ul.bwp.srs.rs.set.rsType.set(srs_rs_set_rs_type = enums.SrsRsSetRsTypeAll.APER, channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default, srsRsrcSet = repcap.SrsRsrcSet.Default) \n
		Sets the SRS transmission type. \n
			:param srs_rs_set_rs_type: PER| APER| SP Supported is only PER (periodic) SRS transmission.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param srsRsrcSet: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Set')"""
		param = Conversions.enum_scalar_to_str(srs_rs_set_rs_type, enums.SrsRsSetRsTypeAll)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		srsRsrcSet_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSet, repcap.SrsRsrcSet)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:SRS:RS:SET{srsRsrcSet_cmd_val}:RSTYpe {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, srsRsrcSet=repcap.SrsRsrcSet.Default) -> enums.SrsRsSetRsTypeAll:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:SRS:RS:SET<GR>:RSTYpe \n
		Snippet: value: enums.SrsRsSetRsTypeAll = driver.source.bb.nr5G.ubwp.user.cell.ul.bwp.srs.rs.set.rsType.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default, srsRsrcSet = repcap.SrsRsrcSet.Default) \n
		Sets the SRS transmission type. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param srsRsrcSet: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Set')
			:return: srs_rs_set_rs_type: PER| APER| SP Supported is only PER (periodic) SRS transmission."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		srsRsrcSet_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSet, repcap.SrsRsrcSet)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:SRS:RS:SET{srsRsrcSet_cmd_val}:RSTYpe?')
		return Conversions.str_to_scalar_enum(response, enums.SrsRsSetRsTypeAll)
