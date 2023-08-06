from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mindex:
	"""Mindex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mindex", core, parent)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, antennaPortMap=repcap.AntennaPortMap.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:POSition:APMap<DIR>:MINDex \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.sspbch.position.apMap.mindex.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, antennaPortMap = repcap.AntennaPortMap.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')
			:param antennaPortMap: optional repeated capability selector. Default value: Nr0 (settable in the interface 'ApMap')
			:return: apmap_idx: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		antennaPortMap_cmd_val = self._base.get_repcap_cmd_value(antennaPortMap, repcap.AntennaPortMap)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:POSition:APMap{antennaPortMap_cmd_val}:MINDex?')
		return Conversions.str_to_int(response)
