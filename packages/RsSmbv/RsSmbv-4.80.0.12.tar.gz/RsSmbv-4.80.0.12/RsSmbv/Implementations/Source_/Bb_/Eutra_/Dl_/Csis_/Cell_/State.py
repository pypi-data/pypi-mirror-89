from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, csi_rs_state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:STATe \n
		Snippet: driver.source.bb.eutra.dl.csis.cell.state.set(csi_rs_state = False, channel = repcap.Channel.Default) \n
		Enables the transmission of a CSI-RS. \n
			:param csi_rs_state: OFF| ON| 1| 0
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.bool_to_str(csi_rs_state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:STATe \n
		Snippet: value: bool = driver.source.bb.eutra.dl.csis.cell.state.get(channel = repcap.Channel.Default) \n
		Enables the transmission of a CSI-RS. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: csi_rs_state: OFF| ON| 1| 0"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
