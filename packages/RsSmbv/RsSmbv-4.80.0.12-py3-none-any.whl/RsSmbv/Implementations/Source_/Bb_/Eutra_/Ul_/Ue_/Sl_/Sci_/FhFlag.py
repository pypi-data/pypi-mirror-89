from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FhFlag:
	"""FhFlag commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fhFlag", core, parent)

	def set(self, sl_freq_hopping: bool, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:SCI<CH>:FHFLag \n
		Snippet: driver.source.bb.eutra.ul.ue.sl.sci.fhFlag.set(sl_freq_hopping = False, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the DCI field frequency hopping flag. If enabled, frequency hopping is used for the PSSCH transmission. \n
			:param sl_freq_hopping: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sci')"""
		param = Conversions.bool_to_str(sl_freq_hopping)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:SCI{channel_cmd_val}:FHFLag {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:SCI<CH>:FHFLag \n
		Snippet: value: bool = driver.source.bb.eutra.ul.ue.sl.sci.fhFlag.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the DCI field frequency hopping flag. If enabled, frequency hopping is used for the PSSCH transmission. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sci')
			:return: sl_freq_hopping: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:SCI{channel_cmd_val}:FHFLag?')
		return Conversions.str_to_bool(response)
