from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nack:
	"""Nack commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nack", core, parent)

	def set(self, nack: enums.NfcNack, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:NACK \n
		Snippet: driver.source.bb.nfc.cblock.nack.set(nack = enums.NfcNack.NCK0, channel = repcap.Channel.Default) \n
		Determines the value of NACK. \n
			:param nack: NCK1| NCK0| NCK4| NCK5
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.enum_scalar_to_str(nack, enums.NfcNack)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:NACK {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NfcNack:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:NACK \n
		Snippet: value: enums.NfcNack = driver.source.bb.nfc.cblock.nack.get(channel = repcap.Channel.Default) \n
		Determines the value of NACK. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: nack: NCK1| NCK0| NCK4| NCK5"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:NACK?')
		return Conversions.str_to_scalar_enum(response, enums.NfcNack)
