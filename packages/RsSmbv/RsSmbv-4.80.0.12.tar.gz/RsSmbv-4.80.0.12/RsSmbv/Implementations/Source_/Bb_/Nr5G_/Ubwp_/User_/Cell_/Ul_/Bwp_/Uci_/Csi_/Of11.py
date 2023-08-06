from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Of11:
	"""Of11 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("of11", core, parent)

	def set(self, pusch_uci_csi_of_11: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:UCI:CSI:OF11 \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.ul.bwp.uci.csi.of11.set(pusch_uci_csi_of_11 = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default) \n
		Sets the CSI part 1 (OF10|OF11) and CSI part 2 (OF20|OF21) information offsets, where the OF10|OF20 are used if up to 11
		CSI bits are multiplexed and OF11|OF21 otherwise. \n
			:param pusch_uci_csi_of_11: integer Range: 0 to 18
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')"""
		param = Conversions.decimal_value_to_str(pusch_uci_csi_of_11)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:UCI:CSI:OF11 {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:UCI:CSI:OF11 \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.user.cell.ul.bwp.uci.csi.of11.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default) \n
		Sets the CSI part 1 (OF10|OF11) and CSI part 2 (OF20|OF21) information offsets, where the OF10|OF20 are used if up to 11
		CSI bits are multiplexed and OF11|OF21 otherwise. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:return: pusch_uci_csi_of_11: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:UCI:CSI:OF11?')
		return Conversions.str_to_int(response)
