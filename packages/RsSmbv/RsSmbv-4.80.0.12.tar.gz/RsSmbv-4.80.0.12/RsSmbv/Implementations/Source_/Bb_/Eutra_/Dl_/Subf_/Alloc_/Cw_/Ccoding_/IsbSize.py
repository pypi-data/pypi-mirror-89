from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IsbSize:
	"""IsbSize commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("isbSize", core, parent)

	def set(self, soft_buf_size: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default, codeword=repcap.Codeword.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ALLoc<CH>:[CW<USER>]:CCODing:ISBSize \n
		Snippet: driver.source.bb.eutra.dl.subf.alloc.cw.ccoding.isbSize.set(soft_buf_size = 1, stream = repcap.Stream.Default, channel = repcap.Channel.Default, codeword = repcap.Codeword.Default) \n
		Sets the size of the IR soft buffer. \n
			:param soft_buf_size: integer Range: 800 to 3667200
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param codeword: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cw')"""
		param = Conversions.decimal_value_to_str(soft_buf_size)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		codeword_cmd_val = self._base.get_repcap_cmd_value(codeword, repcap.Codeword)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:CW{codeword_cmd_val}:CCODing:ISBSize {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, codeword=repcap.Codeword.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ALLoc<CH>:[CW<USER>]:CCODing:ISBSize \n
		Snippet: value: int = driver.source.bb.eutra.dl.subf.alloc.cw.ccoding.isbSize.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default, codeword = repcap.Codeword.Default) \n
		Sets the size of the IR soft buffer. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:param codeword: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cw')
			:return: soft_buf_size: integer Range: 800 to 3667200"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		codeword_cmd_val = self._base.get_repcap_cmd_value(codeword, repcap.Codeword)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:CW{codeword_cmd_val}:CCODing:ISBSize?')
		return Conversions.str_to_int(response)
