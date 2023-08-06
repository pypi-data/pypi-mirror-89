from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tlas:
	"""Tlas commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tlas", core, parent)

	def set(self, tlas: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:TLAS \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.tlas.set(tlas = 1.0, channel = repcap.Channel.Default) \n
		Requires 'Mode > GBAS' (LAAS) header information. Sets the value of the broadcast lateral alert limit. \n
			:param tlas: float Range: 0 to 2.54
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.decimal_value_to_str(tlas)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:TLAS {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:TLAS \n
		Snippet: value: float = driver.source.bb.gbas.vdb.mconfig.tlas.get(channel = repcap.Channel.Default) \n
		Requires 'Mode > GBAS' (LAAS) header information. Sets the value of the broadcast lateral alert limit. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: tlas: float Range: 0 to 2.54"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:TLAS?')
		return Conversions.str_to_float(response)
