from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Config:
	"""Config commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("config", core, parent)

	def set(self, configuration: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:ATT<CH>:NIOT:CONFig \n
		Snippet: driver.source.bb.eutra.ul.ue.prach.att.niot.config.set(configuration = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Selects the NPRACH configuration. \n
			:param configuration: integer Range: 0 to 2
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Att')"""
		param = Conversions.decimal_value_to_str(configuration)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PRACh:ATT{channel_cmd_val}:NIOT:CONFig {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:ATT<CH>:NIOT:CONFig \n
		Snippet: value: int = driver.source.bb.eutra.ul.ue.prach.att.niot.config.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Selects the NPRACH configuration. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Att')
			:return: configuration: integer Range: 0 to 2"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PRACh:ATT{channel_cmd_val}:NIOT:CONFig?')
		return Conversions.str_to_int(response)
