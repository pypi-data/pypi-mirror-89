from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dmr2:
	"""Dmr2 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dmr2", core, parent)

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST>]:ALLoc<CH>:PUCCh:DMR2 \n
		Snippet: value: int = driver.source.bb.eutra.ul.subf.alloc.pucch.dmr2.get(stream = repcap.Stream.Default, channel = repcap.Channel.Default) \n
		Queries the index n(2) DMRS. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: pucc_dmrs_2: integer Range: 0 to 6"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:PUCCh:DMR2?')
		return Conversions.str_to_int(response)
