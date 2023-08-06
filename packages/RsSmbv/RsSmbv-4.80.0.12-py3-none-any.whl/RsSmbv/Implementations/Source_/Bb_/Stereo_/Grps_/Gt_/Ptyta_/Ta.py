from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ta:
	"""Ta commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ta", core, parent)

	def set(self, ta: bool, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:STEReo:GRPS:GT<ST>:PTYTa:TA \n
		Snippet: driver.source.bb.stereo.grps.gt.ptyta.ta.set(ta = False, stream = repcap.Stream.Default) \n
		No command help available \n
			:param ta: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gt')"""
		param = Conversions.bool_to_str(ta)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{stream_cmd_val}:PTYTa:TA {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:STEReo:GRPS:GT<ST>:PTYTa:TA \n
		Snippet: value: bool = driver.source.bb.stereo.grps.gt.ptyta.ta.get(stream = repcap.Stream.Default) \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gt')
			:return: ta: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{stream_cmd_val}:PTYTa:TA?')
		return Conversions.str_to_bool(response)
