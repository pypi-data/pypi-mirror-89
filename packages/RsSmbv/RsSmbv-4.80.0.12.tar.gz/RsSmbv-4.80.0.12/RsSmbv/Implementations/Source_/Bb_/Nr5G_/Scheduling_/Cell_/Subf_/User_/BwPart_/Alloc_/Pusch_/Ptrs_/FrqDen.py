from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import enums
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrqDen:
	"""FrqDen commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frqDen", core, parent)

	def set(self, ptrs_freq_density: enums.PtrsFreqDensity, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PUSCh:PTRS:FRQDen \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pusch.ptrs.frqDen.set(ptrs_freq_density = enums.PtrsFreqDensity.FD2, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		No command help available \n
			:param ptrs_freq_density: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.enum_scalar_to_str(ptrs_freq_density, enums.PtrsFreqDensity)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PUSCh:PTRS:FRQDen {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.PtrsFreqDensity:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PUSCh:PTRS:FRQDen \n
		Snippet: value: enums.PtrsFreqDensity = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pusch.ptrs.frqDen.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: ptrs_freq_density: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PUSCh:PTRS:FRQDen?')
		return Conversions.str_to_scalar_enum(response, enums.PtrsFreqDensity)
