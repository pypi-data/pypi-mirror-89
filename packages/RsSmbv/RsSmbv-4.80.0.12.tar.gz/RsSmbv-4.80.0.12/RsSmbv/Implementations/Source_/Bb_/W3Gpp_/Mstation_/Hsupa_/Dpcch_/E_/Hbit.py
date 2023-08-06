from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hbit:
	"""Hbit commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hbit", core, parent)

	def set(self, hbit: bool, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPCCh:E:HBIT \n
		Snippet: driver.source.bb.w3Gpp.mstation.hsupa.dpcch.e.hbit.set(hbit = False, stream = repcap.Stream.Default) \n
		The command activates the happy bit. \n
			:param hbit: ON| OFF
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.bool_to_str(hbit)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPCCh:E:HBIT {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPCCh:E:HBIT \n
		Snippet: value: bool = driver.source.bb.w3Gpp.mstation.hsupa.dpcch.e.hbit.get(stream = repcap.Stream.Default) \n
		The command activates the happy bit. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: hbit: ON| OFF"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPCCh:E:HBIT?')
		return Conversions.str_to_bool(response)
