from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mark_mode: enums.C5GmarkMode, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:OFDM:TRIGger:OUTPut<CH>:MODE \n
		Snippet: driver.source.bb.ofdm.trigger.output.mode.set(mark_mode = enums.C5GmarkMode.RESTart, channel = repcap.Channel.Default) \n
		Defines the signal for the selected marker output. \n
			:param mark_mode: RESTart
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.enum_scalar_to_str(mark_mode, enums.C5GmarkMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:TRIGger:OUTPut{channel_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.C5GmarkMode:
		"""SCPI: [SOURce<HW>]:BB:OFDM:TRIGger:OUTPut<CH>:MODE \n
		Snippet: value: enums.C5GmarkMode = driver.source.bb.ofdm.trigger.output.mode.get(channel = repcap.Channel.Default) \n
		Defines the signal for the selected marker output. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: mark_mode: RESTart"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:TRIGger:OUTPut{channel_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.C5GmarkMode)
