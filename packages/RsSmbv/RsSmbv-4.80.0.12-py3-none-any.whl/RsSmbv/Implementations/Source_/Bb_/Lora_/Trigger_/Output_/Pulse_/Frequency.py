from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:LORA:TRIGger:OUTPut<CH>:PULSe:FREQuency \n
		Snippet: value: float = driver.source.bb.lora.trigger.output.pulse.frequency.get(channel = repcap.Channel.Default) \n
		Queries the pulse frequency. The return value depends on the pulse divider, which is the sample rate divided by the pulse
		divider. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: frequency: float Range: 2 to 1024"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:LORA:TRIGger:OUTPut{channel_cmd_val}:PULSe:FREQuency?')
		return Conversions.str_to_float(response)
