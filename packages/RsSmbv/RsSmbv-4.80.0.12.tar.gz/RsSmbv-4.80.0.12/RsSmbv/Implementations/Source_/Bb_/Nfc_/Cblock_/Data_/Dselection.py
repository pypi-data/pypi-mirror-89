from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dselection:
	"""Dselection commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dselection", core, parent)

	def set(self, dselection: str, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:DATA:DSELection \n
		Snippet: driver.source.bb.nfc.cblock.data.dselection.set(dselection = '1', channel = repcap.Channel.Default) \n
		Selects a Data List. \n
			:param dselection: string
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.value_to_quoted_str(dselection)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:DATA:DSELection {param}')

	def get(self, channel=repcap.Channel.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:DATA:DSELection \n
		Snippet: value: str = driver.source.bb.nfc.cblock.data.dselection.get(channel = repcap.Channel.Default) \n
		Selects a Data List. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: dselection: string"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:DATA:DSELection?')
		return trim_str_response(response)
