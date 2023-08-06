from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Plength:
	"""Plength commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("plength", core, parent)

	def set(self, payload_length: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:FPGeneric:PLENgth \n
		Snippet: driver.source.bb.nfc.cblock.fpGeneric.plength.set(payload_length = 1, channel = repcap.Channel.Default) \n
		Sets the length of a standard frame. \n
			:param payload_length: integer Range: 1 to 8
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.decimal_value_to_str(payload_length)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:FPGeneric:PLENgth {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:FPGeneric:PLENgth \n
		Snippet: value: int = driver.source.bb.nfc.cblock.fpGeneric.plength.get(channel = repcap.Channel.Default) \n
		Sets the length of a standard frame. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: payload_length: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:FPGeneric:PLENgth?')
		return Conversions.str_to_int(response)
