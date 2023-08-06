from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rpdf:
	"""Rpdf commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rpdf", core, parent)

	def set(self, rpdf: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:RPDF \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.rpdf.set(rpdf = 1, channel = repcap.Channel.Default) \n
		Sets the reference path data selector for FAS. \n
			:param rpdf: integer Range: 0 to 48
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.decimal_value_to_str(rpdf)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:RPDF {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:RPDF \n
		Snippet: value: int = driver.source.bb.gbas.vdb.mconfig.rpdf.get(channel = repcap.Channel.Default) \n
		Sets the reference path data selector for FAS. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: rpdf: integer Range: 0 to 48"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:RPDF?')
		return Conversions.str_to_int(response)
