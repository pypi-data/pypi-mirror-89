from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pointa:
	"""Pointa commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pointa", core, parent)

	def set(self, lte_offs_to_point_a: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:LTE:POINta \n
		Snippet: driver.source.bb.nr5G.node.cell.lte.pointa.set(lte_offs_to_point_a = 1, channel = repcap.Channel.Default) \n
		Sets the LTE carrier center subcarrier location. \n
			:param lte_offs_to_point_a: integer Range: 0 to 30300
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(lte_offs_to_point_a)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:LTE:POINta {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:LTE:POINta \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.lte.pointa.get(channel = repcap.Channel.Default) \n
		Sets the LTE carrier center subcarrier location. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: lte_offs_to_point_a: integer Range: 0 to 30300"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:LTE:POINta?')
		return Conversions.str_to_int(response)
