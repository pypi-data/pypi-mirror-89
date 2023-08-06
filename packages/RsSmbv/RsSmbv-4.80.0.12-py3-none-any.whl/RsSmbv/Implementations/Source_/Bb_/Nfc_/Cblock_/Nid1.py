from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nid1:
	"""Nid1 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nid1", core, parent)

	def set(self, nfcid_1: List[str], channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:NID1 \n
		Snippet: driver.source.bb.nfc.cblock.nid1.set(nfcid_1 = ['raw1', 'raw2', 'raw3'], channel = repcap.Channel.Default) \n
		Determines the entire value of NFCID1. \n
			:param nfcid_1: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.list_to_csv_str(nfcid_1)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:NID1 {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:NID1 \n
		Snippet: value: List[str] = driver.source.bb.nfc.cblock.nid1.get(channel = repcap.Channel.Default) \n
		Determines the entire value of NFCID1. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: nfcid_1: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:NID1?')
		return Conversions.str_to_str_list(response)
