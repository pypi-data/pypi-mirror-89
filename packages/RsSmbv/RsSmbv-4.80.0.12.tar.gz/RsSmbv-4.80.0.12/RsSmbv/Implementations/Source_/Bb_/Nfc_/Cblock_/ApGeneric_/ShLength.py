from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ShLength:
	"""ShLength commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("shLength", core, parent)

	def set(self, short_frame_len: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:APGeneric:SHLength \n
		Snippet: driver.source.bb.nfc.cblock.apGeneric.shLength.set(short_frame_len = 1, channel = repcap.Channel.Default) \n
		Sets the length of a short frame in bits. \n
			:param short_frame_len: integer Range: 1 to 7
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.decimal_value_to_str(short_frame_len)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:APGeneric:SHLength {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:APGeneric:SHLength \n
		Snippet: value: int = driver.source.bb.nfc.cblock.apGeneric.shLength.get(channel = repcap.Channel.Default) \n
		Sets the length of a short frame in bits. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: short_frame_len: integer Range: 1 to 7"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:APGeneric:SHLength?')
		return Conversions.str_to_int(response)
