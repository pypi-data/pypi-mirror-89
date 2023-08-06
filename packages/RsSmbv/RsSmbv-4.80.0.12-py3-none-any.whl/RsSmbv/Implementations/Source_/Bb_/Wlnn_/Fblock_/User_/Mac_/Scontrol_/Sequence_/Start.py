from typing import List

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Start:
	"""Start commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("start", core, parent)

	def set(self, start: List[str], channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:SCONtrol:SEQuence:STARt \n
		Snippet: driver.source.bb.wlnn.fblock.user.mac.scontrol.sequence.start.set(start = ['raw1', 'raw2', 'raw3'], channel = repcap.Channel.Default, availableUser = repcap.AvailableUser.Default) \n
		The command enters the start number of the fragment bits of the sequence control. \n
			:param start: integer Range: #H000,12 to #HFFF,12
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')"""
		param = Conversions.list_to_csv_str(start)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MAC:SCONtrol:SEQuence:STARt {param}')

	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:SCONtrol:SEQuence:STARt \n
		Snippet: value: List[str] = driver.source.bb.wlnn.fblock.user.mac.scontrol.sequence.start.get(channel = repcap.Channel.Default, availableUser = repcap.AvailableUser.Default) \n
		The command enters the start number of the fragment bits of the sequence control. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: start: integer Range: #H000,12 to #HFFF,12"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MAC:SCONtrol:SEQuence:STARt?')
		return Conversions.str_to_str_list(response)
