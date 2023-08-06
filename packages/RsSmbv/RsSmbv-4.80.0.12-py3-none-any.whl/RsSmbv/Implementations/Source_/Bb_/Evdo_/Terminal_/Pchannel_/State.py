from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TERMinal<ST>:PCHannel:STATe \n
		Snippet: value: bool = driver.source.bb.evdo.terminal.pchannel.state.get(stream = repcap.Stream.Default) \n
		Displays the state of the pilot channel. Note: The pilot channel is always switched on. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:return: state: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:PCHannel:STATe?')
		return Conversions.str_to_bool(response)
