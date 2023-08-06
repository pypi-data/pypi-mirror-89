from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Prtt:
	"""Prtt commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("prtt", core, parent)

	def set(self, transition_time: float, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:PRTT \n
		Snippet: driver.source.bb.eutra.ul.ue.prach.prtt.set(transition_time = 1.0, stream = repcap.Stream.Default) \n
		Defines the transition time from beginning of the extended preamble to the start of the preamble itself. \n
			:param transition_time: float Range: 0 to 3E-5, Unit: s
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.decimal_value_to_str(transition_time)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PRACh:PRTT {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:PRTT \n
		Snippet: value: float = driver.source.bb.eutra.ul.ue.prach.prtt.get(stream = repcap.Stream.Default) \n
		Defines the transition time from beginning of the extended preamble to the start of the preamble itself. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: transition_time: float Range: 0 to 3E-5, Unit: s"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PRACh:PRTT?')
		return Conversions.str_to_float(response)
