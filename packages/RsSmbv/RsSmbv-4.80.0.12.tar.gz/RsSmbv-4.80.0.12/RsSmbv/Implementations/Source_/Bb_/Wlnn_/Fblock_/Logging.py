from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Logging:
	"""Logging commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("logging", core, parent)

	def set(self, logging_state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:LOGGing \n
		Snippet: driver.source.bb.wlnn.fblock.logging.set(logging_state = False, channel = repcap.Channel.Default) \n
		If enabled (ON) , the contents of HE-SIG-A and HE-SIG-B fields are written to a file in a text form. The location of the
		file can be queried with method RsSmbv.Source.Bb.Wlnn.Fblock.Logging.set. \n
			:param logging_state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.bool_to_str(logging_state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:LOGGing {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:LOGGing \n
		Snippet: value: bool = driver.source.bb.wlnn.fblock.logging.get(channel = repcap.Channel.Default) \n
		If enabled (ON) , the contents of HE-SIG-A and HE-SIG-B fields are written to a file in a text form. The location of the
		file can be queried with method RsSmbv.Source.Bb.Wlnn.Fblock.Logging.set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: logging_state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:LOGGing?')
		return Conversions.str_to_bool(response)
