from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class View:
	"""View commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("view", core, parent)

	def get_bis(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:VIEW:BIS \n
		Snippet: value: bool = driver.source.bb.eutra.ul.view.get_bis() \n
		No command help available \n
			:return: block_info: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:VIEW:BIS?')
		return Conversions.str_to_bool(response)

	def set_bis(self, block_info: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:VIEW:BIS \n
		Snippet: driver.source.bb.eutra.ul.view.set_bis(block_info = False) \n
		No command help available \n
			:param block_info: No help available
		"""
		param = Conversions.bool_to_str(block_info)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:VIEW:BIS {param}')

	# noinspection PyTypeChecker
	def get_cindex(self) -> enums.EutraCcIndex:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:VIEW:CINDex \n
		Snippet: value: enums.EutraCcIndex = driver.source.bb.eutra.ul.view.get_cindex() \n
		No command help available \n
			:return: dl_tp_cell_idx: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:VIEW:CINDex?')
		return Conversions.str_to_scalar_enum(response, enums.EutraCcIndex)

	def set_cindex(self, dl_tp_cell_idx: enums.EutraCcIndex) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:VIEW:CINDex \n
		Snippet: driver.source.bb.eutra.ul.view.set_cindex(dl_tp_cell_idx = enums.EutraCcIndex.PC) \n
		No command help available \n
			:param dl_tp_cell_idx: No help available
		"""
		param = Conversions.enum_scalar_to_str(dl_tp_cell_idx, enums.EutraCcIndex)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:VIEW:CINDex {param}')

	def get_fsts(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:VIEW:FSTS \n
		Snippet: value: int = driver.source.bb.eutra.ul.view.get_fsts() \n
		No command help available \n
			:return: fsts: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:VIEW:FSTS?')
		return Conversions.str_to_int(response)

	def set_fsts(self, fsts: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:VIEW:FSTS \n
		Snippet: driver.source.bb.eutra.ul.view.set_fsts(fsts = 1) \n
		No command help available \n
			:param fsts: No help available
		"""
		param = Conversions.decimal_value_to_str(fsts)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:VIEW:FSTS {param}')

	def get_viss(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:VIEW:VISS \n
		Snippet: value: int = driver.source.bb.eutra.ul.view.get_viss() \n
		No command help available \n
			:return: viss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:VIEW:VISS?')
		return Conversions.str_to_int(response)

	def set_viss(self, viss: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:VIEW:VISS \n
		Snippet: driver.source.bb.eutra.ul.view.set_viss(viss = 1) \n
		No command help available \n
			:param viss: No help available
		"""
		param = Conversions.decimal_value_to_str(viss)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:VIEW:VISS {param}')
