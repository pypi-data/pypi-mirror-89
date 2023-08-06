from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rmeasurement:
	"""Rmeasurement commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rmeasurement", core, parent)

	def set(self, rmeasurement: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:CAPability:RMEasurement \n
		Snippet: driver.source.bb.wlnn.fblock.bfConfiguration.capability.rmeasurement.set(rmeasurement = False, channel = repcap.Channel.Default) \n
		Informs the associated stations if radio measurement is supported. \n
			:param rmeasurement: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.bool_to_str(rmeasurement)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:BFConfiguration:CAPability:RMEasurement {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:CAPability:RMEasurement \n
		Snippet: value: bool = driver.source.bb.wlnn.fblock.bfConfiguration.capability.rmeasurement.get(channel = repcap.Channel.Default) \n
		Informs the associated stations if radio measurement is supported. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: rmeasurement: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:BFConfiguration:CAPability:RMEasurement?')
		return Conversions.str_to_bool(response)
