from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setting:
	"""Setting commands group definition. 5 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("setting", core, parent)

	@property
	def store(self):
		"""store commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_store'):
			from .Setting_.Store import Store
			self._store = Store(self._core, self._base)
		return self._store

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLAN:SETTing:CATalog \n
		Snippet: value: List[str] = driver.source.bb.wlan.setting.get_catalog() \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_delete(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLAN:SETTing:DELete \n
		Snippet: value: str = driver.source.bb.wlan.setting.get_delete() \n
		No command help available \n
			:return: filename: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:SETTing:DELete?')
		return trim_str_response(response)

	def set_delete(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:SETTing:DELete \n
		Snippet: driver.source.bb.wlan.setting.set_delete(filename = '1') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:SETTing:DELete {param}')

	def load(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAN:SETTing:LOAD \n
		Snippet: driver.source.bb.wlan.setting.load(filename = '1') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:SETTing:LOAD {param}')

	def clone(self) -> 'Setting':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Setting(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
