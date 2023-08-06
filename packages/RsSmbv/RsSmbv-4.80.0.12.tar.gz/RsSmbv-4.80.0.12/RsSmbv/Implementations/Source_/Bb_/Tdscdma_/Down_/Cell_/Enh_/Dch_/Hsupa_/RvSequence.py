from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.Utilities import trim_str_response
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RvSequence:
	"""RvSequence commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rvSequence", core, parent)

	def set(self, rv_sequence: str, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSUPA:RVSequence \n
		Snippet: driver.source.bb.tdscdma.down.cell.enh.dch.hsupa.rvSequence.set(rv_sequence = '1', stream = repcap.Stream.Default) \n
		For HARQ mode set to constant NACK, sets the retransmission sequence. For HSUPA, the command is a query only. \n
			:param rv_sequence: string of 30 coma-separated values The sequence length determines the maximum number of retransmissions. New data is retrieved from the data source after reaching the end of the sequence.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.value_to_quoted_str(rv_sequence)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:HSUPA:RVSequence {param}')

	def get(self, stream=repcap.Stream.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSUPA:RVSequence \n
		Snippet: value: str = driver.source.bb.tdscdma.down.cell.enh.dch.hsupa.rvSequence.get(stream = repcap.Stream.Default) \n
		For HARQ mode set to constant NACK, sets the retransmission sequence. For HSUPA, the command is a query only. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: rv_sequence: string of 30 coma-separated values The sequence length determines the maximum number of retransmissions. New data is retrieved from the data source after reaching the end of the sequence."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:HSUPA:RVSequence?')
		return trim_str_response(response)
