from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tbsi:
	"""Tbsi commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tbsi", core, parent)

	def set(self, chan_cod_tbs_index: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH>:CCODing:TBSI \n
		Snippet: driver.source.bb.eutra.dl.emtc.alloc.ccoding.tbsi.set(chan_cod_tbs_index = 1, channel = repcap.Channel.Default) \n
		Queries the resulting transport block size index. \n
			:param chan_cod_tbs_index: integer Range: 34 to 34
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.decimal_value_to_str(chan_cod_tbs_index)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{channel_cmd_val}:CCODing:TBSI {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH>:CCODing:TBSI \n
		Snippet: value: int = driver.source.bb.eutra.dl.emtc.alloc.ccoding.tbsi.get(channel = repcap.Channel.Default) \n
		Queries the resulting transport block size index. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: chan_cod_tbs_index: integer Range: 34 to 34"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{channel_cmd_val}:CCODing:TBSI?')
		return Conversions.str_to_int(response)
