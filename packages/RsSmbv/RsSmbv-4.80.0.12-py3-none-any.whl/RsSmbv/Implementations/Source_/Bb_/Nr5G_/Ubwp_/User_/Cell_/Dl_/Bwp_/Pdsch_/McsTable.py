from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import enums
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class McsTable:
	"""McsTable commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcsTable", core, parent)

	def set(self, pdsch_mcs_table: enums.McsTable, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:PDSCh:MCSTable \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.dl.bwp.pdsch.mcsTable.set(pdsch_mcs_table = enums.McsTable.QAM256, channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default) \n
		Sets the MCS table and defines the used modulation scheme. \n
			:param pdsch_mcs_table: QAM64| QAM256| QAM64LSE
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')"""
		param = Conversions.enum_scalar_to_str(pdsch_mcs_table, enums.McsTable)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:PDSCh:MCSTable {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> enums.McsTable:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:PDSCh:MCSTable \n
		Snippet: value: enums.McsTable = driver.source.bb.nr5G.ubwp.user.cell.dl.bwp.pdsch.mcsTable.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default) \n
		Sets the MCS table and defines the used modulation scheme. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:return: pdsch_mcs_table: QAM64| QAM256| QAM64LSE"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:PDSCh:MCSTable?')
		return Conversions.str_to_scalar_enum(response, enums.McsTable)
