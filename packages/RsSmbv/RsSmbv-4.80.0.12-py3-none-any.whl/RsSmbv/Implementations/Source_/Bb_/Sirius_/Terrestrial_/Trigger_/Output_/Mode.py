from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.SiriusTerrMarkMode, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:SIRius:TERRestrial:TRIGger:OUTPut<CH>:MODE \n
		Snippet: driver.source.bb.sirius.terrestrial.trigger.output.mode.set(mode = enums.SiriusTerrMarkMode.FRAMe, channel = repcap.Channel.Default) \n
		No command help available \n
			:param mode: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.enum_scalar_to_str(mode, enums.SiriusTerrMarkMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:SIRius:TERRestrial:TRIGger:OUTPut{channel_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.SiriusTerrMarkMode:
		"""SCPI: [SOURce<HW>]:BB:SIRius:TERRestrial:TRIGger:OUTPut<CH>:MODE \n
		Snippet: value: enums.SiriusTerrMarkMode = driver.source.bb.sirius.terrestrial.trigger.output.mode.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: mode: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:SIRius:TERRestrial:TRIGger:OUTPut{channel_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.SiriusTerrMarkMode)
