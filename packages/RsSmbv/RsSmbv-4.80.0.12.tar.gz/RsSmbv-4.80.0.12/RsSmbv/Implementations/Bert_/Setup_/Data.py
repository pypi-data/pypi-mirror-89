from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	# noinspection PyTypeChecker
	def get_polarity(self) -> enums.NormInv:
		"""SCPI: BERT:SETup:DATA:[POLarity] \n
		Snippet: value: enums.NormInv = driver.bert.setup.data.get_polarity() \n
		Sets the polarity of the feedback data bits. \n
			:return: polarity: NORMal| INVerted NORMal High level represents a logic 1, low level a logic 0. INVerted Low level represents a logic 1, high level a logic 0.
		"""
		response = self._core.io.query_str('BERT:SETup:DATA:POLarity?')
		return Conversions.str_to_scalar_enum(response, enums.NormInv)

	def set_polarity(self, polarity: enums.NormInv) -> None:
		"""SCPI: BERT:SETup:DATA:[POLarity] \n
		Snippet: driver.bert.setup.data.set_polarity(polarity = enums.NormInv.INVerted) \n
		Sets the polarity of the feedback data bits. \n
			:param polarity: NORMal| INVerted NORMal High level represents a logic 1, low level a logic 0. INVerted Low level represents a logic 1, high level a logic 0.
		"""
		param = Conversions.enum_scalar_to_str(polarity, enums.NormInv)
		self._core.io.write(f'BERT:SETup:DATA:POLarity {param}')
