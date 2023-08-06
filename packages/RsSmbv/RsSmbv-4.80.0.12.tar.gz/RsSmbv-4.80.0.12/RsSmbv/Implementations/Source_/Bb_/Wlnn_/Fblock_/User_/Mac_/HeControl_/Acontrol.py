from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Acontrol:
	"""Acontrol commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("acontrol", core, parent)

	def set(self, aggregated_ctrl: List[str], channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:HEControl:ACONtrol \n
		Snippet: driver.source.bb.wlnn.fblock.user.mac.heControl.acontrol.set(aggregated_ctrl = ['raw1', 'raw2', 'raw3'], channel = repcap.Channel.Default, availableUser = repcap.AvailableUser.Default) \n
		Sets the value for the aggregated control field. The length of this value may vary according to the selected control ID
		subfield. \n
			:param aggregated_ctrl: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')"""
		param = Conversions.list_to_csv_str(aggregated_ctrl)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MAC:HEControl:ACONtrol {param}')

	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:HEControl:ACONtrol \n
		Snippet: value: List[str] = driver.source.bb.wlnn.fblock.user.mac.heControl.acontrol.get(channel = repcap.Channel.Default, availableUser = repcap.AvailableUser.Default) \n
		Sets the value for the aggregated control field. The length of this value may vary according to the selected control ID
		subfield. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: aggregated_ctrl: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MAC:HEControl:ACONtrol?')
		return Conversions.str_to_str_list(response)
