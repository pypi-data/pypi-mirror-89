from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UdConf:
	"""UdConf commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("udConf", core, parent)

	def set(self, ulca_tdd_ul_dl_conf: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:CA:CELL<CH>:UDConf \n
		Snippet: driver.source.bb.eutra.ul.ca.cell.udConf.set(ulca_tdd_ul_dl_conf = 1, channel = repcap.Channel.Default) \n
		Sets the Uplink-Downlink Configuration number. \n
			:param ulca_tdd_ul_dl_conf: integer Range: 0 to 6
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(ulca_tdd_ul_dl_conf)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:CA:CELL{channel_cmd_val}:UDConf {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:CA:CELL<CH>:UDConf \n
		Snippet: value: int = driver.source.bb.eutra.ul.ca.cell.udConf.get(channel = repcap.Channel.Default) \n
		Sets the Uplink-Downlink Configuration number. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: ulca_tdd_ul_dl_conf: integer Range: 0 to 6"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:CA:CELL{channel_cmd_val}:UDConf?')
		return Conversions.str_to_int(response)
