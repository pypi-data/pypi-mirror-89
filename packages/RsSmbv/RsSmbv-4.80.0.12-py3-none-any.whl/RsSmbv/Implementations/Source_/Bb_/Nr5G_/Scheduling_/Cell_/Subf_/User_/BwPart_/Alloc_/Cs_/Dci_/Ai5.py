from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ai5:
	"""Ai5 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ai5", core, parent)

	def set(self, alloc_dci_ai_5: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:CS:DCI:AI5 \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cs.dci.ai5.set(alloc_dci_ai_5 = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		No command help available \n
			:param alloc_dci_ai_5: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.decimal_value_to_str(alloc_dci_ai_5)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:CS:DCI:AI5 {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:CS:DCI:AI5 \n
		Snippet: value: int = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cs.dci.ai5.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: alloc_dci_ai_5: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:CS:DCI:AI5?')
		return Conversions.str_to_int(response)
