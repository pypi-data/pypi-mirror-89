from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	def set(self, modulation: enums.ModulationC, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSUPA:MODulation \n
		Snippet: driver.source.bb.tdscdma.down.cell.enh.dch.hsupa.modulation.set(modulation = enums.ModulationC.QAM16, stream = repcap.Stream.Default) \n
		Sets the modulation scheme for each HSDPA RMC or HSUPA FRC. The HSUPA FRCs do not support modulation scheme 64QAM. \n
			:param modulation: QPSK| QAM16| QAM64
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(modulation, enums.ModulationC)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:HSUPA:MODulation {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.ModulationC:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSUPA:MODulation \n
		Snippet: value: enums.ModulationC = driver.source.bb.tdscdma.down.cell.enh.dch.hsupa.modulation.get(stream = repcap.Stream.Default) \n
		Sets the modulation scheme for each HSDPA RMC or HSUPA FRC. The HSUPA FRCs do not support modulation scheme 64QAM. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: modulation: QPSK| QAM16| QAM64"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:HSUPA:MODulation?')
		return Conversions.str_to_scalar_enum(response, enums.ModulationC)
