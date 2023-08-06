from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dpl4:
	"""Dpl4 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dpl4", core, parent)

	def set(self, ta_dpl_4: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:DPL4 \n
		Snippet: driver.source.bb.nfc.cblock.dpl4.set(ta_dpl_4 = False, channel = repcap.Channel.Default) \n
		Enables support of divisor 4 for POLL to LISTEN (Bit Rate Capability) . \n
			:param ta_dpl_4: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.bool_to_str(ta_dpl_4)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:DPL4 {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:DPL4 \n
		Snippet: value: bool = driver.source.bb.nfc.cblock.dpl4.get(channel = repcap.Channel.Default) \n
		Enables support of divisor 4 for POLL to LISTEN (Bit Rate Capability) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: ta_dpl_4: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:DPL4?')
		return Conversions.str_to_bool(response)
