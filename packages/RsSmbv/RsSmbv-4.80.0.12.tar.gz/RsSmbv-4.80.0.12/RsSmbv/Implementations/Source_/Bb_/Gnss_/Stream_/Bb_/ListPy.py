from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ListPy:
	"""ListPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("listPy", core, parent)

	def get(self, stream=repcap.Stream.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:GNSS:STReam<ST>:BB:LIST \n
		Snippet: value: str = driver.source.bb.gnss.stream.bb.listPy.get(stream = repcap.Stream.Default) \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Stream')
			:return: bb_streams: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:STReam{stream_cmd_val}:BB:LIST?')
		return trim_str_response(response)
