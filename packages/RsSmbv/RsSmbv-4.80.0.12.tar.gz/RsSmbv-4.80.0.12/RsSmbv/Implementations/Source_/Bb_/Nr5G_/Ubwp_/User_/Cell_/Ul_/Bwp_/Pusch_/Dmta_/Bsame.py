from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bsame:
	"""Bsame commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bsame", core, parent)

	def set(self, same_dmrs_setting: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:PUSCh:DMTA:BSAMe \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.ul.bwp.pusch.dmta.bsame.set(same_dmrs_setting = False, channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default) \n
		Per default, the same configuration applies for DMRS mapping type A and B. Disable 'Same Settings for Type A and Type B'
		to modify the mapping type B settings. Mapping type A and B define the DMRS position in the PUSCH, the starting symbol
		and length. The UE informs the BS about the mapping type supportability via the UE capability information message. Before
		modifying Mapping Type B settings this state has to be deactivated. \n
			:param same_dmrs_setting: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')"""
		param = Conversions.bool_to_str(same_dmrs_setting)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:PUSCh:DMTA:BSAMe {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:PUSCh:DMTA:BSAMe \n
		Snippet: value: bool = driver.source.bb.nr5G.ubwp.user.cell.ul.bwp.pusch.dmta.bsame.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default) \n
		Per default, the same configuration applies for DMRS mapping type A and B. Disable 'Same Settings for Type A and Type B'
		to modify the mapping type B settings. Mapping type A and B define the DMRS position in the PUSCH, the starting symbol
		and length. The UE informs the BS about the mapping type supportability via the UE capability information message. Before
		modifying Mapping Type B settings this state has to be deactivated. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:return: same_dmrs_setting: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:PUSCh:DMTA:BSAMe?')
		return Conversions.str_to_bool(response)
