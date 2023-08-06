from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cbua:
	"""Cbua commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cbua", core, parent)

	def set(self, cb_use_alt: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:APM:CBUA \n
		Snippet: driver.source.bb.eutra.dl.user.apm.cbua.set(cb_use_alt = False, channel = repcap.Channel.Default) \n
		Applies the enhanced 4 Tx codebook. \n
			:param cb_use_alt: 0| 1| OFF| ON OFF Tthe normal codebook is used. ON Applied is the enhanced 4Tx codebook.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.bool_to_str(cb_use_alt)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:APM:CBUA {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:APM:CBUA \n
		Snippet: value: bool = driver.source.bb.eutra.dl.user.apm.cbua.get(channel = repcap.Channel.Default) \n
		Applies the enhanced 4 Tx codebook. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: cb_use_alt: 0| 1| OFF| ON OFF Tthe normal codebook is used. ON Applied is the enhanced 4Tx codebook."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:APM:CBUA?')
		return Conversions.str_to_bool(response)
