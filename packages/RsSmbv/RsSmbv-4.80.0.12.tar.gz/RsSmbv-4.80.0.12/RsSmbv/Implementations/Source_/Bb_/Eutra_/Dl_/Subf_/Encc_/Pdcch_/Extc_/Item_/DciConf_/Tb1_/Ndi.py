from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ndi:
	"""Ndi commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ndi", core, parent)

	def set(self, new_data_indicat: bool, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:ITEM<CH>:DCIConf:TB1:NDI \n
		Snippet: driver.source.bb.eutra.dl.subf.encc.pdcch.extc.item.dciConf.tb1.ndi.set(new_data_indicat = False, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the DCI Format 2/2A field New Data Indicator. \n
			:param new_data_indicat: ON| OFF
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Item')"""
		param = Conversions.bool_to_str(new_data_indicat)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:ITEM{channel_cmd_val}:DCIConf:TB1:NDI {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:ITEM<CH>:DCIConf:TB1:NDI \n
		Snippet: value: bool = driver.source.bb.eutra.dl.subf.encc.pdcch.extc.item.dciConf.tb1.ndi.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Sets the DCI Format 2/2A field New Data Indicator. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Item')
			:return: new_data_indicat: ON| OFF"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:ITEM{channel_cmd_val}:DCIConf:TB1:NDI?')
		return Conversions.str_to_bool(response)
