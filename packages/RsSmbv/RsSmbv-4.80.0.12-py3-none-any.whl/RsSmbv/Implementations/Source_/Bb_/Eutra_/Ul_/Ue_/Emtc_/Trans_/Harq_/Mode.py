from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.EutraAckNackMode, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:EMTC:TRANs<CH>:HARQ:MODE \n
		Snippet: driver.source.bb.eutra.ul.ue.emtc.trans.harq.mode.set(mode = enums.EutraAckNackMode.BUNDling, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the ACK/NACK mode. \n
			:param mode: MUX
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')"""
		param = Conversions.enum_scalar_to_str(mode, enums.EutraAckNackMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:EMTC:TRANs{channel_cmd_val}:HARQ:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.EutraAckNackMode:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:EMTC:TRANs<CH>:HARQ:MODE \n
		Snippet: value: enums.EutraAckNackMode = driver.source.bb.eutra.ul.ue.emtc.trans.harq.mode.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the ACK/NACK mode. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')
			:return: mode: MUX"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:EMTC:TRANs{channel_cmd_val}:HARQ:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.EutraAckNackMode)
