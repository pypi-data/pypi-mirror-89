from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FromPy:
	"""FromPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fromPy", core, parent)

	def set(self, pcqi_from: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:ROW<CH>:PCQI:FROM \n
		Snippet: driver.source.bb.w3Gpp.mstation.dpcch.hs.row.pcqi.fromPy.set(pcqi_from = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		(Release 8 and later) Defines the beginning / end of the PCI/CQI transmissions inside the PCI/CQI cycle. The range is
		specified in multiples of intervals (Inter-TTI distance) . \n
			:param pcqi_from: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')"""
		param = Conversions.decimal_value_to_str(pcqi_from)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:ROW{channel_cmd_val}:PCQI:FROM {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:ROW<CH>:PCQI:FROM \n
		Snippet: value: int = driver.source.bb.w3Gpp.mstation.dpcch.hs.row.pcqi.fromPy.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		(Release 8 and later) Defines the beginning / end of the PCI/CQI transmissions inside the PCI/CQI cycle. The range is
		specified in multiples of intervals (Inter-TTI distance) . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:return: pcqi_from: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:ROW{channel_cmd_val}:PCQI:FROM?')
		return Conversions.str_to_int(response)
