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
	def get(self, stream=repcap.Stream.Default) -> enums.ModulationD:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:RMC:MODulation \n
		Snippet: value: enums.ModulationD = driver.source.bb.eutra.ul.ue.sl.rmc.modulation.get(stream = repcap.Stream.Default) \n
		Queries the used modulation scheme. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: rmc_modulation: QPSK| QAM16| QAM64| QAM256| QAM1024"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:RMC:MODulation?')
		return Conversions.str_to_scalar_enum(response, enums.ModulationD)
