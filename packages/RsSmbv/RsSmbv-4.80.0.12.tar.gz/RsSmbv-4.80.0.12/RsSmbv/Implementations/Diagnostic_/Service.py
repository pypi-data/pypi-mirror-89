from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Service:
	"""Service commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("service", core, parent)

	def get_sfunction(self) -> str:
		"""SCPI: DIAGnostic<HW>:SERVice:SFUNction \n
		Snippet: value: str = driver.diagnostic.service.get_sfunction() \n
		No command help available \n
			:return: direct_string: No help available
		"""
		response = self._core.io.query_str('DIAGnostic<HwInstance>:SERVice:SFUNction?')
		return trim_str_response(response)

	def set_sfunction(self, direct_string: str) -> None:
		"""SCPI: DIAGnostic<HW>:SERVice:SFUNction \n
		Snippet: driver.diagnostic.service.set_sfunction(direct_string = '1') \n
		No command help available \n
			:param direct_string: No help available
		"""
		param = Conversions.value_to_quoted_str(direct_string)
		self._core.io.write(f'DIAGnostic<HwInstance>:SERVice:SFUNction {param}')

	def get_value(self) -> bool:
		"""SCPI: DIAGnostic:SERVice \n
		Snippet: value: bool = driver.diagnostic.service.get_value() \n
		No command help available \n
			:return: service: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:SERVice?')
		return Conversions.str_to_bool(response)

	def set_value(self, service: bool) -> None:
		"""SCPI: DIAGnostic:SERVice \n
		Snippet: driver.diagnostic.service.set_value(service = False) \n
		No command help available \n
			:param service: No help available
		"""
		param = Conversions.bool_to_str(service)
		self._core.io.write(f'DIAGnostic:SERVice {param}')
