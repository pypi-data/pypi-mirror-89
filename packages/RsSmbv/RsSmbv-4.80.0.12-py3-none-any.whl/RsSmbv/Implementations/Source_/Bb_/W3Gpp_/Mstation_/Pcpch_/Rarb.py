from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rarb:
	"""Rarb commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rarb", core, parent)

	def set(self, state: bool, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:RARB \n
		Snippet: driver.source.bb.w3Gpp.mstation.pcpch.rarb.set(state = False, stream = repcap.Stream.Default) \n
		Enables/disables repeating the selected PCPCH structure during one ARB sequence. \n
			:param state: 0| 1| OFF| ON ON Within one ARB sequence, the selected PCPCH structure is repeated once. OFF The selected PCPCH structure can be repeated several time, depending on the structure length (method RsSmbv.Source.Bb.W3Gpp.Mstation.Prach.Timing.Speriod.get_) and the method RsSmbv.Source.Bb.W3Gpp.Mstation.Pcpch.Rafter.set.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.bool_to_str(state)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:RARB {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:RARB \n
		Snippet: value: bool = driver.source.bb.w3Gpp.mstation.pcpch.rarb.get(stream = repcap.Stream.Default) \n
		Enables/disables repeating the selected PCPCH structure during one ARB sequence. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: state: 0| 1| OFF| ON ON Within one ARB sequence, the selected PCPCH structure is repeated once. OFF The selected PCPCH structure can be repeated several time, depending on the structure length (method RsSmbv.Source.Bb.W3Gpp.Mstation.Prach.Timing.Speriod.get_) and the method RsSmbv.Source.Bb.W3Gpp.Mstation.Pcpch.Rafter.set."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:RARB?')
		return Conversions.str_to_bool(response)
