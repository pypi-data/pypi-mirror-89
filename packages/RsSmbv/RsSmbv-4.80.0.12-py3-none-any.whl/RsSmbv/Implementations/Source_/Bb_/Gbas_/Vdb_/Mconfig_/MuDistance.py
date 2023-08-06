from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MuDistance:
	"""MuDistance commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("muDistance", core, parent)

	def set(self, distance: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:MUDistance \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.muDistance.set(distance = 1.0, channel = repcap.Channel.Default) \n
		Sets the maximum distance from the reference point for which the integrity is assured. \n
			:param distance: float Range: 0 to 510
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.decimal_value_to_str(distance)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:MUDistance {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:MUDistance \n
		Snippet: value: float = driver.source.bb.gbas.vdb.mconfig.muDistance.get(channel = repcap.Channel.Default) \n
		Sets the maximum distance from the reference point for which the integrity is assured. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: distance: float Range: 0 to 510"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:MUDistance?')
		return Conversions.str_to_float(response)
