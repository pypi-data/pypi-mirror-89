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

	def set(self, state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:PLCP:LCBit:STATe \n
		Snippet: driver.source.bb.wlnn.fblock.plcp.lcBit.state.set(state = False, channel = repcap.Channel.Default) \n
		(available only for CCK and PBCC transport modes) Sets the Locked Clock Bit in Service Field of the PLCP Header. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:PLCP:LCBit:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:PLCP:LCBit:STATe \n
		Snippet: value: bool = driver.source.bb.wlnn.fblock.plcp.lcBit.state.get(channel = repcap.Channel.Default) \n
		(available only for CCK and PBCC transport modes) Sets the Locked Clock Bit in Service Field of the PLCP Header. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:PLCP:LCBit:STATe?')
		return Conversions.str_to_bool(response)
