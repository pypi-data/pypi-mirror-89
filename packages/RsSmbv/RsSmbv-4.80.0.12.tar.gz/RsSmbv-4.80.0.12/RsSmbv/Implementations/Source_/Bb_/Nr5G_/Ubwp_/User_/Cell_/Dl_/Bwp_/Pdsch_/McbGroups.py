from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import enums
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class McbGroups:
	"""McbGroups commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcbGroups", core, parent)

	def set(self, dl_max_cbg_per_tb: enums.MaxCbgaLl, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:PDSCh:MCBGroups \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.dl.bwp.pdsch.mcbGroups.set(dl_max_cbg_per_tb = enums.MaxCbgaLl.DISabled, channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default) \n
		Limits the number of code block groups per transport block. In 5G NR a huge TB (transport block) is split into multiple
		code blocks (CB) . Multiples CBs are grouped into one code block group (CBG) . The number of code blocks grouped into the
		CBG can be limited by the 'Max Code Block Groups Per Transport Block' setting. \n
			:param dl_max_cbg_per_tb: G2| G4| DISabled| G6| G8 G2 Limits the number of code block groups per transport block to 2. G4 Limits the number of code block groups per transport block to 4. G6 Limits the number of code block groups per transport block to 6. G8 Limits the number of code block groups per transport block to 8. DISabled Default value (also G0) , which disabled the limitation of code block groups per transport block.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')"""
		param = Conversions.enum_scalar_to_str(dl_max_cbg_per_tb, enums.MaxCbgaLl)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:PDSCh:MCBGroups {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> enums.MaxCbgaLl:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:PDSCh:MCBGroups \n
		Snippet: value: enums.MaxCbgaLl = driver.source.bb.nr5G.ubwp.user.cell.dl.bwp.pdsch.mcbGroups.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, numSuffix = repcap.NumSuffix.Default) \n
		Limits the number of code block groups per transport block. In 5G NR a huge TB (transport block) is split into multiple
		code blocks (CB) . Multiples CBs are grouped into one code block group (CBG) . The number of code blocks grouped into the
		CBG can be limited by the 'Max Code Block Groups Per Transport Block' setting. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:return: dl_max_cbg_per_tb: G2| G4| DISabled| G6| G8 G2 Limits the number of code block groups per transport block to 2. G4 Limits the number of code block groups per transport block to 4. G6 Limits the number of code block groups per transport block to 6. G8 Limits the number of code block groups per transport block to 8. DISabled Default value (also G0) , which disabled the limitation of code block groups per transport block."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:PDSCh:MCBGroups?')
		return Conversions.str_to_scalar_enum(response, enums.MaxCbgaLl)
