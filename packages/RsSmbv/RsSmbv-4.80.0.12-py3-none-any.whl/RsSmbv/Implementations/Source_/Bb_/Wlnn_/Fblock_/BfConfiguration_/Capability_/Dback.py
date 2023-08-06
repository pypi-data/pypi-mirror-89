from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dback:
	"""Dback commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dback", core, parent)

	def set(self, cd_back: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:CAPability:DBACk \n
		Snippet: driver.source.bb.wlnn.fblock.bfConfiguration.capability.dback.set(cd_back = False, channel = repcap.Channel.Default) \n
		Informs the associated stations if delayed block Ack is allowed. \n
			:param cd_back: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.bool_to_str(cd_back)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:BFConfiguration:CAPability:DBACk {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:CAPability:DBACk \n
		Snippet: value: bool = driver.source.bb.wlnn.fblock.bfConfiguration.capability.dback.get(channel = repcap.Channel.Default) \n
		Informs the associated stations if delayed block Ack is allowed. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: cd_back: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:BFConfiguration:CAPability:DBACk?')
		return Conversions.str_to_bool(response)
