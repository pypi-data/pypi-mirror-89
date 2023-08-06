from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Period:
	"""Period commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("period", core, parent)

	def set(self, mark_usr_per: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:TRIGger:OUTPut<CH>:PERiod \n
		Snippet: driver.source.bb.huwb.trigger.output.period.set(mark_usr_per = 1, channel = repcap.Channel.Default) \n
		No command help available \n
			:param mark_usr_per: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(mark_usr_per)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:TRIGger:OUTPut{channel_cmd_val}:PERiod {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:HUWB:TRIGger:OUTPut<CH>:PERiod \n
		Snippet: value: int = driver.source.bb.huwb.trigger.output.period.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: mark_usr_per: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:HUWB:TRIGger:OUTPut{channel_cmd_val}:PERiod?')
		return Conversions.str_to_int(response)
