from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BpMode:
	"""BpMode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bpMode", core, parent)

	def set(self, ebp_mode: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:ERP:BPMode \n
		Snippet: driver.source.bb.wlnn.fblock.bfConfiguration.erp.bpMode.set(ebp_mode = False, channel = repcap.Channel.Default) \n
		Informs associated stations whether to use the long or the short preamble. \n
			:param ebp_mode: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.bool_to_str(ebp_mode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:BFConfiguration:ERP:BPMode {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BFConfiguration:ERP:BPMode \n
		Snippet: value: bool = driver.source.bb.wlnn.fblock.bfConfiguration.erp.bpMode.get(channel = repcap.Channel.Default) \n
		Informs associated stations whether to use the long or the short preamble. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: ebp_mode: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:BFConfiguration:ERP:BPMode?')
		return Conversions.str_to_bool(response)
