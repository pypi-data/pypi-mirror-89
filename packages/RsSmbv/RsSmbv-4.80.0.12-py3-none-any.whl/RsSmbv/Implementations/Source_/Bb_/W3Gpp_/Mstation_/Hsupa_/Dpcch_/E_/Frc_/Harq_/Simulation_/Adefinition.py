from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import enums
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Adefinition:
	"""Adefinition commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("adefinition", core, parent)

	def set(self, adrfinition: enums.LowHigh, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPCCh:E:FRC:HARQ:SIMulation:ADEFinition \n
		Snippet: driver.source.bb.w3Gpp.mstation.hsupa.dpcch.e.frc.harq.simulation.adefinition.set(adrfinition = enums.LowHigh.HIGH, stream = repcap.Stream.Default) \n
		No command help available \n
			:param adrfinition: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(adrfinition, enums.LowHigh)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPCCh:E:FRC:HARQ:SIMulation:ADEFinition {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.LowHigh:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPCCh:E:FRC:HARQ:SIMulation:ADEFinition \n
		Snippet: value: enums.LowHigh = driver.source.bb.w3Gpp.mstation.hsupa.dpcch.e.frc.harq.simulation.adefinition.get(stream = repcap.Stream.Default) \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: adrfinition: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPCCh:E:FRC:HARQ:SIMulation:ADEFinition?')
		return Conversions.str_to_scalar_enum(response, enums.LowHigh)
