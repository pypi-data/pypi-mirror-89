from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Qos:
	"""Qos commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("qos", core, parent)

	def set(self, qos: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:CAPability:QOS \n
		Snippet: driver.source.bb.wlnn.fblock.bfConfiguration.capability.qos.set(qos = False, channel = repcap.Channel.Default) \n
		Informs the associated stations if quality of service (QoS) is supported. \n
			:param qos: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.bool_to_str(qos)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:BFConfiguration:CAPability:QOS {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:CAPability:QOS \n
		Snippet: value: bool = driver.source.bb.wlnn.fblock.bfConfiguration.capability.qos.get(channel = repcap.Channel.Default) \n
		Informs the associated stations if quality of service (QoS) is supported. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: qos: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:BFConfiguration:CAPability:QOS?')
		return Conversions.str_to_bool(response)
