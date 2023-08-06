from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nsym:
	"""Nsym commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nsym", core, parent)

	def set(self, up_pts_num_sym: int, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:PUSCh:UPPTs:NSYM \n
		Snippet: driver.source.bb.eutra.ul.ue.cell.pusch.uppts.nsym.set(up_pts_num_sym = 1, stream = repcap.Stream.Default, carrierComponent = repcap.CarrierComponent.Default) \n
		Sets the number of symbols used for the PUSCH transmission. \n
			:param up_pts_num_sym: integer Range: 1 to 472
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(up_pts_num_sym)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:PUSCh:UPPTs:NSYM {param}')

	def get(self, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:PUSCh:UPPTs:NSYM \n
		Snippet: value: int = driver.source.bb.eutra.ul.ue.cell.pusch.uppts.nsym.get(stream = repcap.Stream.Default, carrierComponent = repcap.CarrierComponent.Default) \n
		Sets the number of symbols used for the PUSCH transmission. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: up_pts_num_sym: integer Range: 1 to 472"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:PUSCh:UPPTs:NSYM?')
		return Conversions.str_to_int(response)
