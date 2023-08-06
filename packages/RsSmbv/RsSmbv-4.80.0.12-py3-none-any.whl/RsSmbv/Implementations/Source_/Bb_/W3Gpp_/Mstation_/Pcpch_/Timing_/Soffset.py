from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Soffset:
	"""Soffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("soffset", core, parent)

	def set(self, so_ffset: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:TIMing:SOFFset \n
		Snippet: driver.source.bb.w3Gpp.mstation.pcpch.timing.soffset.set(so_ffset = 1, stream = repcap.Stream.Default) \n
		This command defines the start offset of the PCPCH in access slots. The starting time delay in timeslots is calculated
		according to: 2 x Start Offset. \n
			:param so_ffset: integer Range: 1 to 14
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(so_ffset)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:TIMing:SOFFset {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:TIMing:SOFFset \n
		Snippet: value: int = driver.source.bb.w3Gpp.mstation.pcpch.timing.soffset.get(stream = repcap.Stream.Default) \n
		This command defines the start offset of the PCPCH in access slots. The starting time delay in timeslots is calculated
		according to: 2 x Start Offset. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: so_ffset: integer Range: 1 to 14"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:TIMing:SOFFset?')
		return Conversions.str_to_int(response)
