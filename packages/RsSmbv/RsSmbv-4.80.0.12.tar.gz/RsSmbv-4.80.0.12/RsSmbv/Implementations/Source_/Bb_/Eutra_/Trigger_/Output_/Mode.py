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

	def set(self, mode: enums.EutraMarkMode, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TRIGger:OUTPut<CH>:MODE \n
		Snippet: driver.source.bb.eutra.trigger.output.mode.set(mode = enums.EutraMarkMode.FAP, channel = repcap.Channel.Default) \n
		Defines the signal for the selected marker output. \n
			:param mode: SUBFram| FRAM| RESTart| PERiod| RATio| FAP| SFNRestart
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.enum_scalar_to_str(mode, enums.EutraMarkMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TRIGger:OUTPut{channel_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraMarkMode:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TRIGger:OUTPut<CH>:MODE \n
		Snippet: value: enums.EutraMarkMode = driver.source.bb.eutra.trigger.output.mode.get(channel = repcap.Channel.Default) \n
		Defines the signal for the selected marker output. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: mode: SUBFram| FRAM| RESTart| PERiod| RATio| FAP| SFNRestart"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:TRIGger:OUTPut{channel_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.EutraMarkMode)
