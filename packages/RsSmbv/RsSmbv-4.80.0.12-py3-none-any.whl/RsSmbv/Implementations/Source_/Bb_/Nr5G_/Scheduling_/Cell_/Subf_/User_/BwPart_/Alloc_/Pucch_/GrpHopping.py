from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import enums
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GrpHopping:
	"""GrpHopping commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("grpHopping", core, parent)

	def set(self, pucch_grp_hopping: enums.PucchGrpHoppingAll, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PUCCh:GRPHopping \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pucch.grpHopping.set(pucch_grp_hopping = enums.PucchGrpHoppingAll.DIS, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the higher-layer parameter pucch-GroupHopping. \n
			:param pucch_grp_hopping: N| ENA| DIS N = neither ENA = enable DIS = disable
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.enum_scalar_to_str(pucch_grp_hopping, enums.PucchGrpHoppingAll)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PUCCh:GRPHopping {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.PucchGrpHoppingAll:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PUCCh:GRPHopping \n
		Snippet: value: enums.PucchGrpHoppingAll = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pucch.grpHopping.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the higher-layer parameter pucch-GroupHopping. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: pucch_grp_hopping: N| ENA| DIS N = neither ENA = enable DIS = disable"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PUCCh:GRPHopping?')
		return Conversions.str_to_scalar_enum(response, enums.PucchGrpHoppingAll)
