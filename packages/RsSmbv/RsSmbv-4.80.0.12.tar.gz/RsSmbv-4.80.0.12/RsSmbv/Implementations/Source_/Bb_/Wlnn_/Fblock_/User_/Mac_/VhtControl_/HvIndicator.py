from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HvIndicator:
	"""HvIndicator commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hvIndicator", core, parent)

	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:VHTControl:HVINdicator \n
		Snippet: value: List[str] = driver.source.bb.wlnn.fblock.user.mac.vhtControl.hvIndicator.get(channel = repcap.Channel.Default, availableUser = repcap.AvailableUser.Default) \n
		The command queries the used format (HT or VHT) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: ht_vht_indicator: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MAC:VHTControl:HVINdicator?')
		return Conversions.str_to_str_list(response)
