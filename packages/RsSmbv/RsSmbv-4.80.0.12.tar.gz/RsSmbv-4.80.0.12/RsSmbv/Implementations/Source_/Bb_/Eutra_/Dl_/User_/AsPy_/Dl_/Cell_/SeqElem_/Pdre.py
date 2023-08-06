from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pdre:
	"""Pdre commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pdre", core, parent)

	def set(self, re_map_qcl: int, channel=repcap.Channel.Default, stream=repcap.Stream.Nr1) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST>:SEQelem:PDRE \n
		Snippet: driver.source.bb.eutra.dl.user.asPy.dl.cell.seqElem.pdre.set(re_map_qcl = 1, channel = repcap.Channel.Default, stream = repcap.Stream.Nr1) \n
		Sets the PDSCH RE mapping and QCL (quasi-co-location) indicator. See also BB:EUTRa:ENCC:PDCCh:EXTC:ITEM<ch0>:DCIConf:PDRE \n
			:param re_map_qcl: integer Range: 0 to 3
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1"""
		param = Conversions.decimal_value_to_str(re_map_qcl)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{stream_cmd_val}:SEQelem:PDRE {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Nr1) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:CELL<ST>:SEQelem:PDRE \n
		Snippet: value: int = driver.source.bb.eutra.dl.user.asPy.dl.cell.seqElem.pdre.get(channel = repcap.Channel.Default, stream = repcap.Stream.Nr1) \n
		Sets the PDSCH RE mapping and QCL (quasi-co-location) indicator. See also BB:EUTRa:ENCC:PDCCh:EXTC:ITEM<ch0>:DCIConf:PDRE \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1
			:return: re_map_qcl: integer Range: 0 to 3"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{stream_cmd_val}:SEQelem:PDRE?')
		return Conversions.str_to_int(response)
