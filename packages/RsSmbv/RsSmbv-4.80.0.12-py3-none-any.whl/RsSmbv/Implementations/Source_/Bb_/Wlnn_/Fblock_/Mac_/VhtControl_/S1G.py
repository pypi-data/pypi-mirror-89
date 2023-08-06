from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class S1G:
	"""S1G commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("s1G", core, parent)

	def set(self, s_1_g: List[str], channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:S1G \n
		Snippet: driver.source.bb.wlnn.fblock.mac.vhtControl.s1G.set(s_1_g = ['raw1', 'raw2', 'raw3'], channel = repcap.Channel.Default) \n
		No command help available \n
			:param s_1_g: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.list_to_csv_str(s_1_g)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:VHTControl:S1G {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:S1G \n
		Snippet: value: List[str] = driver.source.bb.wlnn.fblock.mac.vhtControl.s1G.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: s_1_g: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:MAC:VHTControl:S1G?')
		return Conversions.str_to_str_list(response)
