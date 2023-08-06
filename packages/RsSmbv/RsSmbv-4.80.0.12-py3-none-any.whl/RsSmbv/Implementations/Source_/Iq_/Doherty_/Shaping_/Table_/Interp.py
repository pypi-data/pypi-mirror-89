from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Interp:
	"""Interp commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("interp", core, parent)

	def set(self, ipartnterpolation: enums.Interpolation, stream=repcap.Stream.Default) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty<ST>:SHAPing:TABLe:INTerp \n
		Snippet: driver.source.iq.doherty.shaping.table.interp.set(ipartnterpolation = enums.Interpolation.LINear, stream = repcap.Stream.Default) \n
		No command help available \n
			:param ipartnterpolation: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')"""
		param = Conversions.enum_scalar_to_str(ipartnterpolation, enums.Interpolation)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:SHAPing:TABLe:INTerp {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.Interpolation:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty<ST>:SHAPing:TABLe:INTerp \n
		Snippet: value: enums.Interpolation = driver.source.iq.doherty.shaping.table.interp.get(stream = repcap.Stream.Default) \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')
			:return: ipartnterpolation: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:SHAPing:TABLe:INTerp?')
		return Conversions.str_to_scalar_enum(response, enums.Interpolation)
