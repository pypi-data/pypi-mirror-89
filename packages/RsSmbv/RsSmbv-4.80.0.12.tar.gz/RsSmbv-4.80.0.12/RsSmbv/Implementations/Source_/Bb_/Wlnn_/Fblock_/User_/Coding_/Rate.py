from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rate:
	"""Rate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rate", core, parent)

	def set(self, rate: enums.WlannFbCodRate, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:CODing:RATE \n
		Snippet: driver.source.bb.wlnn.fblock.user.coding.rate.set(rate = enums.WlannFbCodRate.CR1D2, channel = repcap.Channel.Default, availableUser = repcap.AvailableUser.Default) \n
		This command selects the coding rate. \n
			:param rate: CR1D2| CR2D3| CR3D4| CR5D6
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(rate, enums.WlannFbCodRate)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:CODing:RATE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> enums.WlannFbCodRate:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:CODing:RATE \n
		Snippet: value: enums.WlannFbCodRate = driver.source.bb.wlnn.fblock.user.coding.rate.get(channel = repcap.Channel.Default, availableUser = repcap.AvailableUser.Default) \n
		This command selects the coding rate. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: rate: CR1D2| CR2D3| CR3D4| CR5D6"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:CODing:RATE?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbCodRate)
