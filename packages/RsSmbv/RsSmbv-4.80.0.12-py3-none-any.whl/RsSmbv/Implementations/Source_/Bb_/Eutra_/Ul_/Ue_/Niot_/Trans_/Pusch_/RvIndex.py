from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RvIndex:
	"""RvIndex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rvIndex", core, parent)

	def set(self, nbiot_rv_idx: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:TRANs<CH>:PUSCh:RVINdex \n
		Snippet: driver.source.bb.eutra.ul.ue.niot.trans.pusch.rvIndex.set(nbiot_rv_idx = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the starting redundancy version index. \n
			:param nbiot_rv_idx: integer Range: 0 to 2
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')"""
		param = Conversions.decimal_value_to_str(nbiot_rv_idx)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:TRANs{channel_cmd_val}:PUSCh:RVINdex {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:TRANs<CH>:PUSCh:RVINdex \n
		Snippet: value: int = driver.source.bb.eutra.ul.ue.niot.trans.pusch.rvIndex.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the starting redundancy version index. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')
			:return: nbiot_rv_idx: integer Range: 0 to 2"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:TRANs{channel_cmd_val}:PUSCh:RVINdex?')
		return Conversions.str_to_int(response)
