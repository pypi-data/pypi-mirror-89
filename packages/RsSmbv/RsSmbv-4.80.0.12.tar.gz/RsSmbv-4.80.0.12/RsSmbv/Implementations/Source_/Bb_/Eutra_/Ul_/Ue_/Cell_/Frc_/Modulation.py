from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default) -> enums.ModulationB:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:FRC:MODulation \n
		Snippet: value: enums.ModulationB = driver.source.bb.eutra.ul.ue.cell.frc.modulation.get(stream = repcap.Stream.Default, carrierComponent = repcap.CarrierComponent.Default) \n
		Queries the modulation for the selected FRC (BB:EUTRa:UL:FRC:TYPE) . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: modulation: QPSK| QAM16| QAM64| QAM256"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:FRC:MODulation?')
		return Conversions.str_to_scalar_enum(response, enums.ModulationB)
