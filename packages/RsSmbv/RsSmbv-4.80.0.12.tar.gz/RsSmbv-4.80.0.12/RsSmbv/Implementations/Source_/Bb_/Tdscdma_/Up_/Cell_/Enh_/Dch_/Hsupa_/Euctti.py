from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Euctti:
	"""Euctti commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("euctti", core, parent)

	def set(self, euctti: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:HSUPA:EUCTti \n
		Snippet: driver.source.bb.tdscdma.up.cell.enh.dch.hsupa.euctti.set(euctti = 1, stream = repcap.Stream.Default) \n
		Sets the number of E-UCCH channels per TTI. \n
			:param euctti: integer Range: 1 to 8
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(euctti)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:ENH:DCH:HSUPA:EUCTti {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:HSUPA:EUCTti \n
		Snippet: value: int = driver.source.bb.tdscdma.up.cell.enh.dch.hsupa.euctti.get(stream = repcap.Stream.Default) \n
		Sets the number of E-UCCH channels per TTI. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: euctti: integer Range: 1 to 8"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:ENH:DCH:HSUPA:EUCTti?')
		return Conversions.str_to_int(response)
