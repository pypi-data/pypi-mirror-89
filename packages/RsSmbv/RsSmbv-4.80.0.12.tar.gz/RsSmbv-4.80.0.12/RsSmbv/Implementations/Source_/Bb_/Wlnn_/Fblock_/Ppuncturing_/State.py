from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, preamble_punc: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:PPUNcturing:STATe \n
		Snippet: driver.source.bb.wlnn.fblock.ppuncturing.state.set(preamble_punc = False, channel = repcap.Channel.Default) \n
		Enables preamble puncturing of the HE MU PPDU in 80 MHz or (80+80) /160 MHz channels. \n
			:param preamble_punc: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.bool_to_str(preamble_punc)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:PPUNcturing:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:PPUNcturing:STATe \n
		Snippet: value: bool = driver.source.bb.wlnn.fblock.ppuncturing.state.get(channel = repcap.Channel.Default) \n
		Enables preamble puncturing of the HE MU PPDU in 80 MHz or (80+80) /160 MHz channels. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: preamble_punc: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:PPUNcturing:STATe?')
		return Conversions.str_to_bool(response)
