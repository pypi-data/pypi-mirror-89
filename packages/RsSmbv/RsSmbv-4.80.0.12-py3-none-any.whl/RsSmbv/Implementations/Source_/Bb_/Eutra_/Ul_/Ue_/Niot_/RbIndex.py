from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RbIndex:
	"""RbIndex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rbIndex", core, parent)

	def set(self, res_blk_index: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:RBINdex \n
		Snippet: driver.source.bb.eutra.ul.ue.niot.rbIndex.set(res_blk_index = 1, stream = repcap.Stream.Default) \n
		Sets the resource block number in that the NB-IoT transmissions are allocated. \n
			:param res_blk_index: integer Range: Depends on other values
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.decimal_value_to_str(res_blk_index)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:RBINdex {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:RBINdex \n
		Snippet: value: int = driver.source.bb.eutra.ul.ue.niot.rbIndex.get(stream = repcap.Stream.Default) \n
		Sets the resource block number in that the NB-IoT transmissions are allocated. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: res_blk_index: integer Range: Depends on other values"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:RBINdex?')
		return Conversions.str_to_int(response)
