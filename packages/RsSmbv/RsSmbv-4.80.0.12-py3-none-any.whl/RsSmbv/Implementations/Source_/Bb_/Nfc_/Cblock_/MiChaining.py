from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MiChaining:
	"""MiChaining commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("miChaining", core, parent)

	def set(self, mchaining: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:MICHaining \n
		Snippet: driver.source.bb.nfc.cblock.miChaining.set(mchaining = False, channel = repcap.Channel.Default) \n
		Determines if more information (MI) is chained. \n
			:param mchaining: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.bool_to_str(mchaining)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:MICHaining {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:MICHaining \n
		Snippet: value: bool = driver.source.bb.nfc.cblock.miChaining.get(channel = repcap.Channel.Default) \n
		Determines if more information (MI) is chained. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: mchaining: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:MICHaining?')
		return Conversions.str_to_bool(response)
