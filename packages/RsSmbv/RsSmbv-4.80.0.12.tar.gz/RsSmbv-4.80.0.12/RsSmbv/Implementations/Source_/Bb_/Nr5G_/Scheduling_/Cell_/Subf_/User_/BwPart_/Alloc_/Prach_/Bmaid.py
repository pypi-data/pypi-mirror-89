from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bmaid:
	"""Bmaid commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bmaid", core, parent)

	def set(self, ref_level_identif: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PRACh:BMAid \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.prach.bmaid.set(ref_level_identif = False, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the bandwidth of the given allocation as reference for the 'Burst' power mode. \n
			:param ref_level_identif: 0| 1| OFF| ON 0|OFF Disables the given allocation as burst reference for the 'Burst' power mode. 1|ON Sets the given allocation as burst reference for the 'Burst' power mode.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.bool_to_str(ref_level_identif)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PRACh:BMAid {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PRACh:BMAid \n
		Snippet: value: bool = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.prach.bmaid.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Sets the bandwidth of the given allocation as reference for the 'Burst' power mode. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: ref_level_identif: 0| 1| OFF| ON 0|OFF Disables the given allocation as burst reference for the 'Burst' power mode. 1|ON Sets the given allocation as burst reference for the 'Burst' power mode."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PRACh:BMAid?')
		return Conversions.str_to_bool(response)
