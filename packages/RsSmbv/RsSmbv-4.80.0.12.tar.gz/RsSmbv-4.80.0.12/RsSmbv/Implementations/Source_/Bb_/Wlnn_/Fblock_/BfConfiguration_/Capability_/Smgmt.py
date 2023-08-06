from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Smgmt:
	"""Smgmt commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("smgmt", core, parent)

	def set(self, smg_mt: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:CAPability:SMGMt \n
		Snippet: driver.source.bb.wlnn.fblock.bfConfiguration.capability.smgmt.set(smg_mt = False, channel = repcap.Channel.Default) \n
		Informs the associated stations if spectrum management is enabled. \n
			:param smg_mt: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.bool_to_str(smg_mt)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:BFConfiguration:CAPability:SMGMt {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:CAPability:SMGMt \n
		Snippet: value: bool = driver.source.bb.wlnn.fblock.bfConfiguration.capability.smgmt.get(channel = repcap.Channel.Default) \n
		Informs the associated stations if spectrum management is enabled. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: smg_mt: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:BFConfiguration:CAPability:SMGMt?')
		return Conversions.str_to_bool(response)
