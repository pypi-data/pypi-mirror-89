from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sid:
	"""Sid commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sid", core, parent)

	def set(self, scram_ident: bool, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:ITEM<CH>:DCIConf:SID \n
		Snippet: driver.source.bb.eutra.dl.subf.encc.pdcch.extc.item.dciConf.sid.set(scram_ident = False, stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Enables/disables the DCI Format 2B field Scrambling Identity. \n
			:param scram_ident: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Item')"""
		param = Conversions.bool_to_str(scram_ident)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:ITEM{channel_cmd_val}:DCIConf:SID {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:ITEM<CH>:DCIConf:SID \n
		Snippet: value: bool = driver.source.bb.eutra.dl.subf.encc.pdcch.extc.item.dciConf.sid.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Enables/disables the DCI Format 2B field Scrambling Identity. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Item')
			:return: scram_ident: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:ITEM{channel_cmd_val}:DCIConf:SID?')
		return Conversions.str_to_bool(response)
