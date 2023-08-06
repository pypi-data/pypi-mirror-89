from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delay:
	"""Delay commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delay", core, parent)

	def set(self, delay: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:DME:TRIGger:[EXTernal<CH>]:DELay \n
		Snippet: driver.source.bb.dme.trigger.external.delay.set(delay = 1.0, channel = repcap.Channel.Default) \n
		Sets the trigger delay. \n
			:param delay: float Range: 0 to 65535
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'External')"""
		param = Conversions.decimal_value_to_str(delay)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:TRIGger:EXTernal{channel_cmd_val}:DELay {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:DME:TRIGger:[EXTernal<CH>]:DELay \n
		Snippet: value: float = driver.source.bb.dme.trigger.external.delay.get(channel = repcap.Channel.Default) \n
		Sets the trigger delay. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'External')
			:return: delay: float Range: 0 to 65535"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DME:TRIGger:EXTernal{channel_cmd_val}:DELay?')
		return Conversions.str_to_float(response)
