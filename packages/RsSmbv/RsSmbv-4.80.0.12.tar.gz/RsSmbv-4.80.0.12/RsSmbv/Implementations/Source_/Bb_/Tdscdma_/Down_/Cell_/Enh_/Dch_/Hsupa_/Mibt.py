from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mibt:
	"""Mibt commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mibt", core, parent)

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSUPA:MIBT \n
		Snippet: value: float = driver.source.bb.tdscdma.down.cell.enh.dch.hsupa.mibt.get(stream = repcap.Stream.Default) \n
		Queries maximum information bits sent in each TTI before coding. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: mibt: float"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:HSUPA:MIBT?')
		return Conversions.str_to_float(response)
