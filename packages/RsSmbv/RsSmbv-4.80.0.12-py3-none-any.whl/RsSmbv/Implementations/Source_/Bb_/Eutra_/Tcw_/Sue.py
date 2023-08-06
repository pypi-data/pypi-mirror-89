from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sue:
	"""Sue commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sue", core, parent)

	def get_ovrb(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:SUE:OVRB \n
		Snippet: value: int = driver.source.bb.eutra.tcw.sue.get_ovrb() \n
		Sets the number of RB the allocated RB(s) are shifted with. \n
			:return: offset_vrb: integer Range: 0 to 75
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:SUE:OVRB?')
		return Conversions.str_to_int(response)

	def set_ovrb(self, offset_vrb: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:SUE:OVRB \n
		Snippet: driver.source.bb.eutra.tcw.sue.set_ovrb(offset_vrb = 1) \n
		Sets the number of RB the allocated RB(s) are shifted with. \n
			:param offset_vrb: integer Range: 0 to 75
		"""
		param = Conversions.decimal_value_to_str(offset_vrb)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:SUE:OVRB {param}')

	def get_tsrs(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:SUE:TSRS \n
		Snippet: value: bool = driver.source.bb.eutra.tcw.sue.get_tsrs() \n
		No command help available \n
			:return: transmit_srs: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:SUE:TSRS?')
		return Conversions.str_to_bool(response)

	def set_tsrs(self, transmit_srs: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:SUE:TSRS \n
		Snippet: driver.source.bb.eutra.tcw.sue.set_tsrs(transmit_srs = False) \n
		No command help available \n
			:param transmit_srs: No help available
		"""
		param = Conversions.bool_to_str(transmit_srs)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:SUE:TSRS {param}')

	def get_ueid(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:SUE:UEID \n
		Snippet: value: int = driver.source.bb.eutra.tcw.sue.get_ueid() \n
		Sets the UE ID/n_RNTI. \n
			:return: ue_id_nrnti: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:SUE:UEID?')
		return Conversions.str_to_int(response)

	def set_ueid(self, ue_id_nrnti: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:SUE:UEID \n
		Snippet: driver.source.bb.eutra.tcw.sue.set_ueid(ue_id_nrnti = 1) \n
		Sets the UE ID/n_RNTI. \n
			:param ue_id_nrnti: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(ue_id_nrnti)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:SUE:UEID {param}')
