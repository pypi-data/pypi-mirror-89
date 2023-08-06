from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReShift:
	"""ReShift commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("reShift", core, parent)

	def set(self, shift: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:TRIGger:OUTPut<CH>:RESHift \n
		Snippet: driver.source.bb.btooth.trigger.output.reShift.set(shift = 1.0, channel = repcap.Channel.Default) \n
		Shifts the rising edge of the marker the specified number of samples. Negative values result in a shift back of the
		marker edge. \n
			:param shift: float Range: dynamic to dynamic
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(shift)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:TRIGger:OUTPut{channel_cmd_val}:RESHift {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:TRIGger:OUTPut<CH>:RESHift \n
		Snippet: value: float = driver.source.bb.btooth.trigger.output.reShift.get(channel = repcap.Channel.Default) \n
		Shifts the rising edge of the marker the specified number of samples. Negative values result in a shift back of the
		marker edge. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: shift: float Range: dynamic to dynamic"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:TRIGger:OUTPut{channel_cmd_val}:RESHift?')
		return Conversions.str_to_float(response)
