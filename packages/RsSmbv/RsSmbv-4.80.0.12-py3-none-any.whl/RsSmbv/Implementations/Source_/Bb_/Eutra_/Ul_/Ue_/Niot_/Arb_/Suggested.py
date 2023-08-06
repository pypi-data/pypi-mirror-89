from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Suggested:
	"""Suggested commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("suggested", core, parent)

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:ARB:SUGGested \n
		Snippet: value: int = driver.source.bb.eutra.ul.ue.niot.arb.suggested.get(stream = repcap.Stream.Default) \n
		Queries the ARB sequence length that is required for the selected NPUSCH transmissions. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: nbiot_sugg_seq_len: integer Range: 0 to 1E4"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:ARB:SUGGested?')
		return Conversions.str_to_int(response)
