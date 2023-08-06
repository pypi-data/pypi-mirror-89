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

	def set(self, state: bool, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:SCONtrol:STATe \n
		Snippet: driver.source.bb.wlnn.fblock.user.mac.scontrol.state.set(state = False, channel = repcap.Channel.Default, availableUser = repcap.AvailableUser.Default) \n
		The command activates/deactivates the sequence control. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MAC:SCONtrol:STATe {param}')

	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:SCONtrol:STATe \n
		Snippet: value: bool = driver.source.bb.wlnn.fblock.user.mac.scontrol.state.get(channel = repcap.Channel.Default, availableUser = repcap.AvailableUser.Default) \n
		The command activates/deactivates the sequence control. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MAC:SCONtrol:STATe?')
		return Conversions.str_to_bool(response)
