from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Store:
	"""Store commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("store", core, parent)

	def get_fast(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:SETTing:STORe:FAST \n
		Snippet: value: bool = driver.source.bb.pramp.setting.store.get_fast() \n
		No command help available \n
			:return: fast: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:SETTing:STORe:FAST?')
		return Conversions.str_to_bool(response)

	def set_fast(self, fast: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:SETTing:STORe:FAST \n
		Snippet: driver.source.bb.pramp.setting.store.set_fast(fast = False) \n
		No command help available \n
			:param fast: No help available
		"""
		param = Conversions.bool_to_str(fast)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:SETTing:STORe:FAST {param}')

	def set_value(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:SETTing:STORe \n
		Snippet: driver.source.bb.pramp.setting.store.set_value(filename = '1') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:SETTing:STORe {param}')
