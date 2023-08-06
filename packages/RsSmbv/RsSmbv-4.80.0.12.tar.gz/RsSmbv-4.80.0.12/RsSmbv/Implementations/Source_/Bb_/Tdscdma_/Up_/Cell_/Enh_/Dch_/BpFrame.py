from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Utilities import trim_str_response
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BpFrame:
	"""BpFrame commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bpFrame", core, parent)

	def get(self, stream=repcap.Stream.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:BPFRame \n
		Snippet: value: str = driver.source.bb.tdscdma.up.cell.enh.dch.bpFrame.get(stream = repcap.Stream.Default) \n
		Queries the data bits in the DPDCH component of the DPCH frame at physical level. The value depends on the slot format. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: bp_frame: string"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:ENH:DCH:BPFRame?')
		return trim_str_response(response)
