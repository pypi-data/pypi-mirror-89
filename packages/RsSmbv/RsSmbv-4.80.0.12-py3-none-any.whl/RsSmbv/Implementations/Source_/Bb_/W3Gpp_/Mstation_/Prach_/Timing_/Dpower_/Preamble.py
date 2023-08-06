from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Preamble:
	"""Preamble commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("preamble", core, parent)

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PRACh:TIMing:DPOWer:PREamble \n
		Snippet: value: float = driver.source.bb.w3Gpp.mstation.prach.timing.dpower.preamble.get(stream = repcap.Stream.Default) \n
		Queries level correction value for the preamble before the message part. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: preamble: float Range: -80 to 0"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PRACh:TIMing:DPOWer:PREamble?')
		return Conversions.str_to_float(response)
