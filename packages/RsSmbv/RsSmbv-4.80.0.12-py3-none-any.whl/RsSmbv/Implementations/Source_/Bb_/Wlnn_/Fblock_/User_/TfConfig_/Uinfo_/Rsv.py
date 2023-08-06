from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rsv:
	"""Rsv commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rsv", core, parent)

	def set(self, reserved: List[str], channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:TFConfig:UINFo<ST>:RSV \n
		Snippet: driver.source.bb.wlnn.fblock.user.tfConfig.uinfo.rsv.set(reserved = ['raw1', 'raw2', 'raw3'], channel = repcap.Channel.Default, availableUser = repcap.AvailableUser.Default, stream = repcap.Stream.Default) \n
		Sets the value bits of the user info field. You can configure the user info for up to 37 users with the command
		[:SOURce<hw>]:BB:WLNN:FBLock<ch>[:USER<di>]:TFConfig:NUINfo. \n
			:param reserved: 7 bits
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Uinfo')"""
		param = Conversions.list_to_csv_str(reserved)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:TFConfig:UINFo{stream_cmd_val}:RSV {param}')

	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default, stream=repcap.Stream.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:TFConfig:UINFo<ST>:RSV \n
		Snippet: value: List[str] = driver.source.bb.wlnn.fblock.user.tfConfig.uinfo.rsv.get(channel = repcap.Channel.Default, availableUser = repcap.AvailableUser.Default, stream = repcap.Stream.Default) \n
		Sets the value bits of the user info field. You can configure the user info for up to 37 users with the command
		[:SOURce<hw>]:BB:WLNN:FBLock<ch>[:USER<di>]:TFConfig:NUINfo. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Uinfo')
			:return: reserved: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:TFConfig:UINFo{stream_cmd_val}:RSV?')
		return Conversions.str_to_str_list(response)
