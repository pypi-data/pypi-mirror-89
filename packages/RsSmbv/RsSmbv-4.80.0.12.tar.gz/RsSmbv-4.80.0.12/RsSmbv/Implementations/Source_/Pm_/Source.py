from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Source:
	"""Source commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("source", core, parent)

	def set(self, source: enums.AmFmSource, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:PM<CH>:SOURce \n
		Snippet: driver.source.pm.source.set(source = enums.AmFmSource.EXT1, channel = repcap.Channel.Default) \n
		Selects the modulation source for phase modulation signal. \n
			:param source: EXT1| NOISe| LF2| LF1| INTernal| EXTernal LF1|LF2 Uses an internally generated LF signal. EXT1 Uses an externally supplied LF signal. NOISe Uses the internally generated noise signal. INTernal Uses the internally generated signal of LF1. EXTernal Uses an external LF signal (EXT1) .
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pm')"""
		param = Conversions.enum_scalar_to_str(source, enums.AmFmSource)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:PM{channel_cmd_val}:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.AmFmSource:
		"""SCPI: [SOURce<HW>]:PM<CH>:SOURce \n
		Snippet: value: enums.AmFmSource = driver.source.pm.source.get(channel = repcap.Channel.Default) \n
		Selects the modulation source for phase modulation signal. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pm')
			:return: source: EXT1| NOISe| LF2| LF1| INTernal| EXTernal LF1|LF2 Uses an internally generated LF signal. EXT1 Uses an externally supplied LF signal. NOISe Uses the internally generated noise signal. INTernal Uses the internally generated signal of LF1. EXTernal Uses an external LF signal (EXT1) ."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:PM{channel_cmd_val}:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.AmFmSource)
