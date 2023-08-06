from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Inhibit:
	"""Inhibit commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("inhibit", core, parent)

	def set(self, inhibit: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:SIRius:SATellite:TRIGger:[EXTernal<CH>]:INHibit \n
		Snippet: driver.source.bb.sirius.satellite.trigger.external.inhibit.set(inhibit = 1, channel = repcap.Channel.Default) \n
		No command help available \n
			:param inhibit: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'External')"""
		param = Conversions.decimal_value_to_str(inhibit)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:SIRius:SATellite:TRIGger:EXTernal{channel_cmd_val}:INHibit {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:SIRius:SATellite:TRIGger:[EXTernal<CH>]:INHibit \n
		Snippet: value: int = driver.source.bb.sirius.satellite.trigger.external.inhibit.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'External')
			:return: inhibit: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:SIRius:SATellite:TRIGger:EXTernal{channel_cmd_val}:INHibit?')
		return Conversions.str_to_int(response)
