from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import enums
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScSpacing:
	"""ScSpacing commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scSpacing", core, parent)

	def set(self, prach_numerology: enums.PrachNumAll, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PRACh:SCSPacing \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.prach.scSpacing.set(prach_numerology = enums.PrachNumAll.N1_25, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Selects a combination of the subcarrier spacing (SCS) and the cyclic prefix (CP) for PRACH. \n
			:param prach_numerology: N1_25| N5| N15| N30| N60| N120
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.enum_scalar_to_str(prach_numerology, enums.PrachNumAll)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PRACh:SCSPacing {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.PrachNumAll:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PRACh:SCSPacing \n
		Snippet: value: enums.PrachNumAll = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.prach.scSpacing.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Selects a combination of the subcarrier spacing (SCS) and the cyclic prefix (CP) for PRACH. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: prach_numerology: N1_25| N5| N15| N30| N60| N120"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PRACh:SCSPacing?')
		return Conversions.str_to_scalar_enum(response, enums.PrachNumAll)
