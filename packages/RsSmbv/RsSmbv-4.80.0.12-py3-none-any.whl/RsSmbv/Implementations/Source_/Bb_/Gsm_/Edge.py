from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Edge:
	"""Edge commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("edge", core, parent)

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.GsmModTypeEdge:
		"""SCPI: [SOURce<HW>]:BB:GSM:EDGE:FORMat \n
		Snippet: value: enums.GsmModTypeEdge = driver.source.bb.gsm.edge.get_format_py() \n
		The command queries the modulation type in the case of EDGE. The modulation type is permanently set to 8PSK. \n
			:return: format_py: P8EDge
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:EDGE:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.GsmModTypeEdge)
