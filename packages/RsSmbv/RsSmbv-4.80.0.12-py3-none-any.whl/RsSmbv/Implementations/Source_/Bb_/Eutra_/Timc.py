from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Timc:
	"""Timc commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("timc", core, parent)

	# noinspection PyTypeChecker
	def get_nta_offset(self) -> enums.EutraTimcNtAoffs:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TIMC:NTAoffset \n
		Snippet: value: enums.EutraTimcNtAoffs = driver.source.bb.eutra.timc.get_nta_offset() \n
		Sets the parameter NTA offset as defined in the 3GPP TS 36.211. \n
			:return: nta_offset: NTA0| NTA624
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TIMC:NTAoffset?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTimcNtAoffs)

	def set_nta_offset(self, nta_offset: enums.EutraTimcNtAoffs) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TIMC:NTAoffset \n
		Snippet: driver.source.bb.eutra.timc.set_nta_offset(nta_offset = enums.EutraTimcNtAoffs._0) \n
		Sets the parameter NTA offset as defined in the 3GPP TS 36.211. \n
			:param nta_offset: NTA0| NTA624
		"""
		param = Conversions.enum_scalar_to_str(nta_offset, enums.EutraTimcNtAoffs)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TIMC:NTAoffset {param}')
