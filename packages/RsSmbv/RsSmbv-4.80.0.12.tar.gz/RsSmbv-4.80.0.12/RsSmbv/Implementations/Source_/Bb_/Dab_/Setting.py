from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setting:
	"""Setting commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("setting", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:DAB:SETTing:CATalog \n
		Snippet: value: List[str] = driver.source.bb.dab.setting.get_catalog() \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DAB:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, file: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:DAB:SETTing:DELete \n
		Snippet: driver.source.bb.dab.setting.delete(file = '1') \n
		No command help available \n
			:param file: No help available
		"""
		param = Conversions.value_to_quoted_str(file)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:SETTing:DELete {param}')

	def load(self, load: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:DAB:SETTing:LOAD \n
		Snippet: driver.source.bb.dab.setting.load(load = '1') \n
		No command help available \n
			:param load: No help available
		"""
		param = Conversions.value_to_quoted_str(load)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:SETTing:LOAD {param}')

	def set_store(self, store: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:DAB:SETTing:STORe \n
		Snippet: driver.source.bb.dab.setting.set_store(store = '1') \n
		No command help available \n
			:param store: No help available
		"""
		param = Conversions.value_to_quoted_str(store)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:SETTing:STORe {param}')
