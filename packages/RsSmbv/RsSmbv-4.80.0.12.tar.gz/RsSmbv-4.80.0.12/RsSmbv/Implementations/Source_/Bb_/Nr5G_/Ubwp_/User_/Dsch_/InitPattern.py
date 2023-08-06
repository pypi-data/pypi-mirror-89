from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InitPattern:
	"""InitPattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("initPattern", core, parent)

	def set(self, pattern_init: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:DSCH:INITpattern \n
		Snippet: driver.source.bb.nr5G.ubwp.user.dsch.initPattern.set(pattern_init = 1, channel = repcap.Channel.Default) \n
		Sets an initialization value for the second m-sequence in the PN sequence. \n
			:param pattern_init: float Range: 1 to 0x7fffff
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.decimal_value_to_str(pattern_init)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:DSCH:INITpattern {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:DSCH:INITpattern \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.user.dsch.initPattern.get(channel = repcap.Channel.Default) \n
		Sets an initialization value for the second m-sequence in the PN sequence. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: pattern_init: float Range: 1 to 0x7fffff"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:DSCH:INITpattern?')
		return Conversions.str_to_int(response)
