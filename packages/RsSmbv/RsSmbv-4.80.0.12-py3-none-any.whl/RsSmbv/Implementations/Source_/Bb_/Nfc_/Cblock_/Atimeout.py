from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Atimeout:
	"""Atimeout commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("atimeout", core, parent)

	def set(self, atimeout: enums.NfcAtnTmot, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:ATIMeout \n
		Snippet: driver.source.bb.nfc.cblock.atimeout.set(atimeout = enums.NfcAtnTmot.ATN, channel = repcap.Channel.Default) \n
		Only used with PDU type 'supervisory'. Determines whether an 'ATN' (Attention) or 'Timeout' supervisory PDU type is used. \n
			:param atimeout: ATN| TOUT
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.enum_scalar_to_str(atimeout, enums.NfcAtnTmot)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:ATIMeout {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NfcAtnTmot:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:ATIMeout \n
		Snippet: value: enums.NfcAtnTmot = driver.source.bb.nfc.cblock.atimeout.get(channel = repcap.Channel.Default) \n
		Only used with PDU type 'supervisory'. Determines whether an 'ATN' (Attention) or 'Timeout' supervisory PDU type is used. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: atimeout: ATN| TOUT"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:ATIMeout?')
		return Conversions.str_to_scalar_enum(response, enums.NfcAtnTmot)
