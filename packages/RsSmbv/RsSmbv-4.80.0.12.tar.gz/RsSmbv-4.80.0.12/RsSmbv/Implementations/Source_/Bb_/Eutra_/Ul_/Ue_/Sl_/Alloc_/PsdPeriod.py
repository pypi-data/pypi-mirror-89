from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PsdPeriod:
	"""PsdPeriod commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("psdPeriod", core, parent)

	def set(self, psdch_period: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:ALLoc<CH>:PSDPeriod \n
		Snippet: driver.source.bb.eutra.ul.ue.sl.alloc.psdPeriod.set(psdch_period = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		In discovery mode, sets the period of the PSDCH. \n
			:param psdch_period: integer Range: 0 to 100
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.decimal_value_to_str(psdch_period)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:ALLoc{channel_cmd_val}:PSDPeriod {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:ALLoc<CH>:PSDPeriod \n
		Snippet: value: int = driver.source.bb.eutra.ul.ue.sl.alloc.psdPeriod.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		In discovery mode, sets the period of the PSDCH. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: psdch_period: integer Range: 0 to 100"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:ALLoc{channel_cmd_val}:PSDPeriod?')
		return Conversions.str_to_int(response)
