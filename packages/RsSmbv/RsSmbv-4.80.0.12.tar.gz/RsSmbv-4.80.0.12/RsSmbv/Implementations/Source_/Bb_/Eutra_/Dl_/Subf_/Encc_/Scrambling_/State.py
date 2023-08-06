from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:SCRambling:STATe \n
		Snippet: driver.source.bb.eutra.dl.subf.encc.scrambling.state.set(state = False, stream = repcap.Stream.Default) \n
		Enables/disables the scrambling of the enhanced channels. \n
			:param state: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.bool_to_str(state)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:SCRambling:STATe {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:SCRambling:STATe \n
		Snippet: value: bool = driver.source.bb.eutra.dl.subf.encc.scrambling.state.get(stream = repcap.Stream.Default) \n
		Enables/disables the scrambling of the enhanced channels. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: state: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:SCRambling:STATe?')
		return Conversions.str_to_bool(response)
