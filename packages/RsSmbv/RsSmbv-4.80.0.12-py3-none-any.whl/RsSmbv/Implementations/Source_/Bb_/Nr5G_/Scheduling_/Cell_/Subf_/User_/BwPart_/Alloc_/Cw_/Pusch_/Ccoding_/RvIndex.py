from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup
from ..............Internal import Conversions
from .............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RvIndex:
	"""RvIndex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rvIndex", core, parent)

	def set(self, rv_index: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default, codeword=repcap.Codeword.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:[CW<S2US>]:PUSCh:CCODing:RVINdex \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cw.pusch.ccoding.rvIndex.set(rv_index = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Default, codeword = repcap.Codeword.Default) \n
		Sets the redundancy version index. \n
			:param rv_index: integer Range: 1 to 2
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param codeword: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cw')"""
		param = Conversions.decimal_value_to_str(rv_index)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		codeword_cmd_val = self._base.get_repcap_cmd_value(codeword, repcap.Codeword)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:CW{codeword_cmd_val}:PUSCh:CCODing:RVINdex {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, codeword=repcap.Codeword.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:[CW<S2US>]:PUSCh:CCODing:RVINdex \n
		Snippet: value: int = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cw.pusch.ccoding.rvIndex.get(channel = repcap.Channel.Default, stream = repcap.Stream.Default, codeword = repcap.Codeword.Default) \n
		Sets the redundancy version index. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param codeword: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cw')
			:return: rv_index: integer Range: 1 to 2"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		codeword_cmd_val = self._base.get_repcap_cmd_value(codeword, repcap.Codeword)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:CW{codeword_cmd_val}:PUSCh:CCODing:RVINdex?')
		return Conversions.str_to_int(response)
