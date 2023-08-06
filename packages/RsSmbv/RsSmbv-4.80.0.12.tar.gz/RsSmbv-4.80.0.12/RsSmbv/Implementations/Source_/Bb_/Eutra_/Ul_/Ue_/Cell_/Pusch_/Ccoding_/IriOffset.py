from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IriOffset:
	"""IriOffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("iriOffset", core, parent)

	def set(self, iri_offset: int, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:PUSCh:CCODing:IRIoffset \n
		Snippet: driver.source.bb.eutra.ul.ue.cell.pusch.ccoding.iriOffset.set(iri_offset = 1, stream = repcap.Stream.Default, carrierComponent = repcap.CarrierComponent.Default) \n
		Sets the RI offset index for control information MCS offset determination. \n
			:param iri_offset: integer Range: 0 to 12
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(iri_offset)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:PUSCh:CCODing:IRIoffset {param}')

	def get(self, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:PUSCh:CCODing:IRIoffset \n
		Snippet: value: int = driver.source.bb.eutra.ul.ue.cell.pusch.ccoding.iriOffset.get(stream = repcap.Stream.Default, carrierComponent = repcap.CarrierComponent.Default) \n
		Sets the RI offset index for control information MCS offset determination. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: iri_offset: integer Range: 0 to 12"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:PUSCh:CCODing:IRIoffset?')
		return Conversions.str_to_int(response)
