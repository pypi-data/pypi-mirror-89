from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Usch:
	"""Usch commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("usch", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:UDTX:USCH:CATalog \n
		Snippet: value: List[str] = driver.source.bb.w3Gpp.mstation.udtx.usch.get_catalog() \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:USCH:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:UDTX:USCH:DELete \n
		Snippet: driver.source.bb.w3Gpp.mstation.udtx.usch.delete(filename = '1') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:USCH:DELete {param}')

	def get_fselect(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:UDTX:USCH:FSELect \n
		Snippet: value: str = driver.source.bb.w3Gpp.mstation.udtx.usch.get_fselect() \n
		No command help available \n
			:return: filename: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:USCH:FSELect?')
		return trim_str_response(response)

	def set_fselect(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:UDTX:USCH:FSELect \n
		Snippet: driver.source.bb.w3Gpp.mstation.udtx.usch.set_fselect(filename = '1') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:USCH:FSELect {param}')
