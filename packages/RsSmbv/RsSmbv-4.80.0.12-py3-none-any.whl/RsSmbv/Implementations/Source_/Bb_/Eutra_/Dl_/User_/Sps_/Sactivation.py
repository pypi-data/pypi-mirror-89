from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sactivation:
	"""Sactivation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sactivation", core, parent)

	def set(self, usr_sps_act_subfr: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:SPS:SACTivation \n
		Snippet: driver.source.bb.eutra.dl.user.sps.sactivation.set(usr_sps_act_subfr = 1, channel = repcap.Channel.Default) \n
		Defines the start and end subframes of the semi-persistent scheduling. \n
			:param usr_sps_act_subfr: integer Range: 0 to 65535
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.decimal_value_to_str(usr_sps_act_subfr)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:SPS:SACTivation {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:SPS:SACTivation \n
		Snippet: value: int = driver.source.bb.eutra.dl.user.sps.sactivation.get(channel = repcap.Channel.Default) \n
		Defines the start and end subframes of the semi-persistent scheduling. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: usr_sps_act_subfr: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:SPS:SACTivation?')
		return Conversions.str_to_int(response)
