from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PhysBits:
	"""PhysBits commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("physBits", core, parent)

	def get(self, carrierComponent=repcap.CarrierComponent.Default, stream=repcap.Stream.Default, channel=repcap.Channel.Default, codeword=repcap.Codeword.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:[CELL<CCIDX>]:[SUBF<ST>]:ALLoc<CH>:[CW<CWID>]:PUSCh:PHYSbits \n
		Snippet: value: int = driver.source.bb.eutra.ul.cell.subf.alloc.cw.pusch.physBits.get(carrierComponent = repcap.CarrierComponent.Default, stream = repcap.Stream.Default, channel = repcap.Channel.Default, codeword = repcap.Codeword.Default) \n
		Queries the number of physical bits for the selected allocation. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param codeword: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cw')
			:return: pusc_phys_bits: integer Range: -1 to 105600"""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		codeword_cmd_val = self._base.get_repcap_cmd_value(codeword, repcap.Codeword)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:CELL{carrierComponent_cmd_val}:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:CW{codeword_cmd_val}:PUSCh:PHYSbits?')
		return Conversions.str_to_int(response)
