from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, chan_cod_state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH>:CCODing:STATe \n
		Snippet: driver.source.bb.eutra.dl.emtc.alloc.ccoding.state.set(chan_cod_state = False, channel = repcap.Channel.Default) \n
		Enables channel coding. \n
			:param chan_cod_state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.bool_to_str(chan_cod_state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{channel_cmd_val}:CCODing:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH>:CCODing:STATe \n
		Snippet: value: bool = driver.source.bb.eutra.dl.emtc.alloc.ccoding.state.get(channel = repcap.Channel.Default) \n
		Enables channel coding. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: chan_cod_state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{channel_cmd_val}:CCODing:STATe?')
		return Conversions.str_to_bool(response)
