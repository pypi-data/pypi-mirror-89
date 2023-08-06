from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PrState:
	"""PrState commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("prState", core, parent)

	def set(self, state: bool, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:PRSTate \n
		Snippet: driver.source.bb.eutra.ul.ue.prach.prState.set(state = False, stream = repcap.Stream.Default) \n
		Activates Power Ramping for the PRACH preamble. The start and the end of the preamble is cyclically extended and
		multiplied with a ramping function (sin^2) . \n
			:param state: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.bool_to_str(state)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PRACh:PRSTate {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:PRSTate \n
		Snippet: value: bool = driver.source.bb.eutra.ul.ue.prach.prState.get(stream = repcap.Stream.Default) \n
		Activates Power Ramping for the PRACH preamble. The start and the end of the preamble is cyclically extended and
		multiplied with a ramping function (sin^2) . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: state: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PRACh:PRSTate?')
		return Conversions.str_to_bool(response)
