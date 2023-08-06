from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bchk:
	"""Bchk commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bchk", core, parent)

	def set(self, bcheck: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:BCHK \n
		Snippet: driver.source.bb.nfc.cblock.bchk.set(bcheck = 1, channel = repcap.Channel.Default) \n
		Determines the format and value of the Maximum Response Time Information MRTICHECK and MRTIUPDATE. \n
			:param bcheck: integer Range: 0 to 3
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.decimal_value_to_str(bcheck)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:BCHK {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:BCHK \n
		Snippet: value: int = driver.source.bb.nfc.cblock.bchk.get(channel = repcap.Channel.Default) \n
		Determines the format and value of the Maximum Response Time Information MRTICHECK and MRTIUPDATE. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: bcheck: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:BCHK?')
		return Conversions.str_to_int(response)
