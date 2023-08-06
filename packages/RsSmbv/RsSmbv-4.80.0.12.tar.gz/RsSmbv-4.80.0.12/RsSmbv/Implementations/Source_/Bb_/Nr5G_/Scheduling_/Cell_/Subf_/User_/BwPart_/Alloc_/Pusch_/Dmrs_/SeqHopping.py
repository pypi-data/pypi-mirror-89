from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import enums
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SeqHopping:
	"""SeqHopping commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("seqHopping", core, parent)

	def set(self, dmrs_grp_seq_hopp: enums.PuschGrpSeqAll, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PUSCh:DMRS:SEQHopping \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pusch.dmrs.seqHopping.set(dmrs_grp_seq_hopp = enums.PuschGrpSeqAll.GRP, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the higher-layer parameter groupOrSequenceHopping that defines the sequence group, required for the DMRS sequence
		generation according to . \n
			:param dmrs_grp_seq_hopp: NEITher| GRP| SEQuence NEITher Disables the group and sequence hopping for the DMRS sequence generation. GRP Enables the group hopping for the DMRS sequence generation. SEQuence Enables the sequence hopping for the DMRS sequence generation.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.enum_scalar_to_str(dmrs_grp_seq_hopp, enums.PuschGrpSeqAll)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PUSCh:DMRS:SEQHopping {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.PuschGrpSeqAll:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PUSCh:DMRS:SEQHopping \n
		Snippet: value: enums.PuschGrpSeqAll = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pusch.dmrs.seqHopping.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the higher-layer parameter groupOrSequenceHopping that defines the sequence group, required for the DMRS sequence
		generation according to . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: dmrs_grp_seq_hopp: NEITher| GRP| SEQuence NEITher Disables the group and sequence hopping for the DMRS sequence generation. GRP Enables the group hopping for the DMRS sequence generation. SEQuence Enables the sequence hopping for the DMRS sequence generation."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PUSCh:DMRS:SEQHopping?')
		return Conversions.str_to_scalar_enum(response, enums.PuschGrpSeqAll)
