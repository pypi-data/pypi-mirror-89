from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rutype:
	"""Rutype commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rutype", core, parent)

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> enums.WlannFbPpduUserRuType:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:USER<DI>:RUTYpe \n
		Snippet: value: enums.WlannFbPpduUserRuType = driver.source.bb.wlnn.fblock.user.rutype.get(channel = repcap.Channel.Default, availableUser = repcap.AvailableUser.Default) \n
		Queries the resource unit type for the current user. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: ru_type: 26| 52| 106| 242| 484| 996| 2996| C26"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:RUTYpe?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbPpduUserRuType)
