from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pad0:
	"""Pad0 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pad0", core, parent)

	def set(self, pad_0: List[str], channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:PAD0 \n
		Snippet: driver.source.bb.nfc.cblock.pad0.set(pad_0 = ['raw1', 'raw2', 'raw3'], channel = repcap.Channel.Default) \n
		Sets the value of PAD0/PAD1/PAD2 (hex) . \n
			:param pad_0: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.list_to_csv_str(pad_0)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:PAD0 {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:PAD0 \n
		Snippet: value: List[str] = driver.source.bb.nfc.cblock.pad0.get(channel = repcap.Channel.Default) \n
		Sets the value of PAD0/PAD1/PAD2 (hex) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: pad_0: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:PAD0?')
		return Conversions.str_to_str_list(response)
