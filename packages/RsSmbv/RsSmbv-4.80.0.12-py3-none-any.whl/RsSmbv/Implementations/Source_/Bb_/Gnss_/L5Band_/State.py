from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, l_5_band_state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:L5Band<CH>:[STATe] \n
		Snippet: driver.source.bb.gnss.l5Band.state.set(l_5_band_state = False, channel = repcap.Channel.Default) \n
		Activates the RF band. \n
			:param l_5_band_state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'L5Band')"""
		param = Conversions.bool_to_str(l_5_band_state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:L5Band{channel_cmd_val}:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:L5Band<CH>:[STATe] \n
		Snippet: value: bool = driver.source.bb.gnss.l5Band.state.get(channel = repcap.Channel.Default) \n
		Activates the RF band. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'L5Band')
			:return: l_5_band_state: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:L5Band{channel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
