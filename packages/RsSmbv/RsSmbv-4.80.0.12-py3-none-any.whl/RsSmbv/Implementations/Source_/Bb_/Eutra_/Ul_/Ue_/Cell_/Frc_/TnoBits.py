from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TnoBits:
	"""TnoBits commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tnoBits", core, parent)

	def get(self, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:FRC:TNOBits \n
		Snippet: value: int = driver.source.bb.eutra.ul.ue.cell.frc.tnoBits.get(stream = repcap.Stream.Default, carrierComponent = repcap.CarrierComponent.Default) \n
		Queries the total number of physical bits available for the PUSCH allocation per subframe in case the PUSCH is not
		shortened because of SRS or because it is transmitted in a cell-specific SRS subframe. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: total_bit_count: integer Range: 0 to max"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:FRC:TNOBits?')
		return Conversions.str_to_int(response)
