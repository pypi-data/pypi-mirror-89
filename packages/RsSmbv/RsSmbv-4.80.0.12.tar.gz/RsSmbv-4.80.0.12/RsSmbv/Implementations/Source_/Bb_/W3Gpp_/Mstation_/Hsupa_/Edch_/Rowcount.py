from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rowcount:
	"""Rowcount commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rowcount", core, parent)

	def set(self, row_count: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:EDCH:ROWCount \n
		Snippet: driver.source.bb.w3Gpp.mstation.hsupa.edch.rowcount.set(row_count = 1, stream = repcap.Stream.Default) \n
		Sets the number of the rows in the scheduling table. \n
			:param row_count: integer Range: 1 to 32
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(row_count)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:EDCH:ROWCount {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:EDCH:ROWCount \n
		Snippet: value: int = driver.source.bb.w3Gpp.mstation.hsupa.edch.rowcount.get(stream = repcap.Stream.Default) \n
		Sets the number of the rows in the scheduling table. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: row_count: integer Range: 1 to 32"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:EDCH:ROWCount?')
		return Conversions.str_to_int(response)
