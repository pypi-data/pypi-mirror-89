from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class To:
	"""To commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("to", core, parent)

	def set(self, hack_to: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:ROW<CH>:HACK:TO \n
		Snippet: driver.source.bb.w3Gpp.mstation.dpcch.hs.row.hack.to.set(hack_to = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		(Release 8 and later) Defines the beginning / end of the HARQ-ACK transmissions inside the HARQ-ACK cycle. R&S SMBVBThe
		range is specified in multiples of intervals (Inter-TTI distance) . \n
			:param hack_to: integer Range: 0 to dynamic
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')"""
		param = Conversions.decimal_value_to_str(hack_to)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:ROW{channel_cmd_val}:HACK:TO {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:ROW<CH>:HACK:TO \n
		Snippet: value: int = driver.source.bb.w3Gpp.mstation.dpcch.hs.row.hack.to.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		(Release 8 and later) Defines the beginning / end of the HARQ-ACK transmissions inside the HARQ-ACK cycle. R&S SMBVBThe
		range is specified in multiples of intervals (Inter-TTI distance) . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:return: hack_to: integer Range: 0 to dynamic"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:ROW{channel_cmd_val}:HACK:TO?')
		return Conversions.str_to_int(response)
