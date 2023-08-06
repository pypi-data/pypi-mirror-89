from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Inhibit:
	"""Inhibit commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("inhibit", core, parent)

	def set(self, inhibit: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:TRIGger:[EXTernal<CH>]:INHibit \n
		Snippet: driver.source.bb.wlan.trigger.external.inhibit.set(inhibit = 1.0, channel = repcap.Channel.Default) \n
		No command help available \n
			:param inhibit: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'External')"""
		param = Conversions.decimal_value_to_str(inhibit)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:TRIGger:EXTernal{channel_cmd_val}:INHibit {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:WLAN:TRIGger:[EXTernal<CH>]:INHibit \n
		Snippet: value: float = driver.source.bb.wlan.trigger.external.inhibit.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'External')
			:return: inhibit: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLAN:TRIGger:EXTernal{channel_cmd_val}:INHibit?')
		return Conversions.str_to_float(response)
