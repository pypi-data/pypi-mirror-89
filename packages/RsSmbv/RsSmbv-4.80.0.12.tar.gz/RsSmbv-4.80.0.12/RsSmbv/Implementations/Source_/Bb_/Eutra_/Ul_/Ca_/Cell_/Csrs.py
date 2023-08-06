from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Csrs:
	"""Csrs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("csrs", core, parent)

	def set(self, ulca_srs_csrs: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:CA:CELL<CH>:CSRS \n
		Snippet: driver.source.bb.eutra.ul.ca.cell.csrs.set(ulca_srs_csrs = 1, channel = repcap.Channel.Default) \n
		Sets the parameter SRS Bandwidth Configuration per component carrier. \n
			:param ulca_srs_csrs: integer Range: 0 to 7
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(ulca_srs_csrs)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:CA:CELL{channel_cmd_val}:CSRS {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:CA:CELL<CH>:CSRS \n
		Snippet: value: int = driver.source.bb.eutra.ul.ca.cell.csrs.get(channel = repcap.Channel.Default) \n
		Sets the parameter SRS Bandwidth Configuration per component carrier. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: ulca_srs_csrs: integer Range: 0 to 7"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:CA:CELL{channel_cmd_val}:CSRS?')
		return Conversions.str_to_int(response)
