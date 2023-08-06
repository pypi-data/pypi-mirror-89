from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OffsetInd:
	"""OffsetInd commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("offsetInd", core, parent)

	def set(self, offset_ind: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:SYNC:OFFSetind \n
		Snippet: driver.source.bb.eutra.ul.ue.sl.sync.offsetInd.set(offset_ind = 1, stream = repcap.Stream.Default) \n
		Sets the parameter syncOffsetIndicator. \n
			:param offset_ind: integer Range: 0 to 159
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.decimal_value_to_str(offset_ind)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:SYNC:OFFSetind {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:SYNC:OFFSetind \n
		Snippet: value: int = driver.source.bb.eutra.ul.ue.sl.sync.offsetInd.get(stream = repcap.Stream.Default) \n
		Sets the parameter syncOffsetIndicator. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: offset_ind: integer Range: 0 to 159"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:SYNC:OFFSetind?')
		return Conversions.str_to_int(response)
