from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tci:
	"""Tci commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tci", core, parent)

	def set(self, nr_5_gcstci_in_dci: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:CS:TCI \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cs.tci.set(nr_5_gcstci_in_dci = False, channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Enables support of quasi co-location TCI field in DCI format 1_1. \n
			:param nr_5_gcstci_in_dci: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.bool_to_str(nr_5_gcstci_in_dci)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:CS:TCI {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:CS:TCI \n
		Snippet: value: bool = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cs.tci.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default) \n
		Enables support of quasi co-location TCI field in DCI format 1_1. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: nr_5_gcstci_in_dci: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:CS:TCI?')
		return Conversions.str_to_bool(response)
