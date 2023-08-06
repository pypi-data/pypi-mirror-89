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

	def set(self, cu_ap_srs_state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:ASRS:STATe \n
		Snippet: driver.source.bb.eutra.dl.user.asrs.state.set(cu_ap_srs_state = False, channel = repcap.Channel.Default) \n
		Enables/disables an aperiodic transmission of SRS for the selected user. \n
			:param cu_ap_srs_state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.bool_to_str(cu_ap_srs_state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:ASRS:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:ASRS:STATe \n
		Snippet: value: bool = driver.source.bb.eutra.dl.user.asrs.state.get(channel = repcap.Channel.Default) \n
		Enables/disables an aperiodic transmission of SRS for the selected user. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: cu_ap_srs_state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:ASRS:STATe?')
		return Conversions.str_to_bool(response)
