from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Repeat:
	"""Repeat commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("repeat", core, parent)

	def set(self, pcqi_rep: int, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:PCQI:REPeat \n
		Snippet: driver.source.bb.w3Gpp.mstation.dpcch.hs.pcqi.repeat.set(pcqi_rep = 1, stream = repcap.Stream.Default) \n
		(Release 8 and Later) Defines the cycle length after that the information in the HS-DPCCH scheduling table is read out
		again from the beginning. \n
			:param pcqi_rep: integer Range: 1 to dynamic
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(pcqi_rep)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:PCQI:REPeat {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:PCQI:REPeat \n
		Snippet: value: int = driver.source.bb.w3Gpp.mstation.dpcch.hs.pcqi.repeat.get(stream = repcap.Stream.Default) \n
		(Release 8 and Later) Defines the cycle length after that the information in the HS-DPCCH scheduling table is read out
		again from the beginning. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: pcqi_rep: integer Range: 1 to dynamic"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:PCQI:REPeat?')
		return Conversions.str_to_int(response)
