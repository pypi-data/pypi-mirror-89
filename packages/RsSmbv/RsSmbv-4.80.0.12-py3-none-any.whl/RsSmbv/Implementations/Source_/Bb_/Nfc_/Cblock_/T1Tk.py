from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class T1Tk:
	"""T1Tk commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("t1Tk", core, parent)

	def set(self, t_1_totk: List[str], channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:T1TK \n
		Snippet: driver.source.bb.nfc.cblock.t1Tk.set(t_1_totk = ['raw1', 'raw2', 'raw3'], channel = repcap.Channel.Default) \n
		For number of historical bytes k greater than 0: sets the historical bytes T1 to Tk. \n
			:param t_1_totk: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.list_to_csv_str(t_1_totk)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:T1TK {param}')

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:T1TK \n
		Snippet: value: List[str] = driver.source.bb.nfc.cblock.t1Tk.get(channel = repcap.Channel.Default) \n
		For number of historical bytes k greater than 0: sets the historical bytes T1 to Tk. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: t_1_totk: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:T1TK?')
		return Conversions.str_to_str_list(response)
