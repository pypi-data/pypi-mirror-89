from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mcs:
	"""Mcs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcs", core, parent)

	def set(self, mcs: enums.WlannFbMcs, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MCS \n
		Snippet: driver.source.bb.wlnn.fblock.user.mcs.set(mcs = enums.WlannFbMcs.MCS0, channel = repcap.Channel.Default, availableUser = repcap.AvailableUser.Default) \n
		Selects the modulation and coding scheme for the spatial streams. \n
			:param mcs: MCS0| MCS1| MCS2| MCS3| MCS4| MCS5| MCS6| MCS7| MCS8| MCS9| MCS10| MCS11| MCS12| MCS13| MCS14| MCS15| MCS16| MCS17| MCS18| MCS19| MCS20| MCS21| MCS22| MCS23| MCS24| MCS25| MCS26| MCS27| MCS28| MCS29| MCS30| MCS31| MCS32| MCS33| MCS34| MCS35| MCS36| MCS37| MCS38| MCS39| MCS40| MCS41| MCS42| MCS43| MCS44| MCS45| MCS46| MCS47| MCS48| MCS49| MCS50| MCS51| MCS52| MCS53| MCS54| MCS55| MCS56| MCS57| MCS58| MCS59| MCS60| MCS61| MCS62| MCS63| MCS64| MCS65| MCS66| MCS67| MCS68| MCS69| MCS70| MCS71| MCS72| MCS73| MCS74| MCS75| MCS76
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(mcs, enums.WlannFbMcs)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MCS {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default) -> enums.WlannFbMcs:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MCS \n
		Snippet: value: enums.WlannFbMcs = driver.source.bb.wlnn.fblock.user.mcs.get(channel = repcap.Channel.Default, availableUser = repcap.AvailableUser.Default) \n
		Selects the modulation and coding scheme for the spatial streams. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: mcs: MCS0| MCS1| MCS2| MCS3| MCS4| MCS5| MCS6| MCS7| MCS8| MCS9| MCS10| MCS11| MCS12| MCS13| MCS14| MCS15| MCS16| MCS17| MCS18| MCS19| MCS20| MCS21| MCS22| MCS23| MCS24| MCS25| MCS26| MCS27| MCS28| MCS29| MCS30| MCS31| MCS32| MCS33| MCS34| MCS35| MCS36| MCS37| MCS38| MCS39| MCS40| MCS41| MCS42| MCS43| MCS44| MCS45| MCS46| MCS47| MCS48| MCS49| MCS50| MCS51| MCS52| MCS53| MCS54| MCS55| MCS56| MCS57| MCS58| MCS59| MCS60| MCS61| MCS62| MCS63| MCS64| MCS65| MCS66| MCS67| MCS68| MCS69| MCS70| MCS71| MCS72| MCS73| MCS74| MCS75| MCS76"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MCS?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbMcs)
