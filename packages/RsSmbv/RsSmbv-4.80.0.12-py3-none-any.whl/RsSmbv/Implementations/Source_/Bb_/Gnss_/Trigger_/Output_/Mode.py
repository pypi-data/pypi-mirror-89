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

	def set(self, mode: enums.MarkModeGnss, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TRIGger:OUTPut<CH>:MODE \n
		Snippet: driver.source.bb.gnss.trigger.output.mode.set(mode = enums.MarkModeGnss.PATTern, channel = repcap.Channel.Default) \n
		Defines the signal for the selected marker output. \n
			:param mode: PULSe| PATTern| RATio| PPS| PP2S| PPS10
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.enum_scalar_to_str(mode, enums.MarkModeGnss)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TRIGger:OUTPut{channel_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.MarkModeGnss:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TRIGger:OUTPut<CH>:MODE \n
		Snippet: value: enums.MarkModeGnss = driver.source.bb.gnss.trigger.output.mode.get(channel = repcap.Channel.Default) \n
		Defines the signal for the selected marker output. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: mode: PULSe| PATTern| RATio| PPS| PP2S| PPS10"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:TRIGger:OUTPut{channel_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.MarkModeGnss)
