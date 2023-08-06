from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class H16Qam:
	"""H16Qam commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("h16Qam", core, parent)

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.GsmModType16Qam:
		"""SCPI: [SOURce<HW>]:BB:GSM:H16Qam:FORMat \n
		Snippet: value: enums.GsmModType16Qam = driver.source.bb.gsm.h16Qam.get_format_py() \n
		The command queries the modulation type. \n
			:return: format_py: QAM16EDge
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:H16Qam:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.GsmModType16Qam)
