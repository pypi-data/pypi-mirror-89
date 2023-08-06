from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sts:
	"""Sts commands group definition. 5 total commands, 0 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sts", core, parent)

	def get_cpart(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:HUWB:STS:CPARt \n
		Snippet: value: List[str] = driver.source.bb.huwb.sts.get_cpart() \n
		Sets the counter part of the V valued. The value is a 32-bit value in hexadecimal representation. \n
			:return: counter_part: integer
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:STS:CPARt?')
		return Conversions.str_to_str_list(response)

	def set_cpart(self, counter_part: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:STS:CPARt \n
		Snippet: driver.source.bb.huwb.sts.set_cpart(counter_part = ['raw1', 'raw2', 'raw3']) \n
		Sets the counter part of the V valued. The value is a 32-bit value in hexadecimal representation. \n
			:param counter_part: integer
		"""
		param = Conversions.list_to_csv_str(counter_part)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:STS:CPARt {param}')

	# noinspection PyTypeChecker
	def get_dlen(self) -> enums.HrpUwbStsDeltaLen:
		"""SCPI: [SOURce<HW>]:BB:HUWB:STS:DLEN \n
		Snippet: value: enums.HrpUwbStsDeltaLen = driver.source.bb.huwb.sts.get_dlen() \n
		Queries the delta length of the scrambled timestamp sequence (STS) . \n
			:return: delta_length: DL_4| DL_8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:STS:DLEN?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbStsDeltaLen)

	def set_dlen(self, delta_length: enums.HrpUwbStsDeltaLen) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:STS:DLEN \n
		Snippet: driver.source.bb.huwb.sts.set_dlen(delta_length = enums.HrpUwbStsDeltaLen.DL_4) \n
		Queries the delta length of the scrambled timestamp sequence (STS) . \n
			:param delta_length: DL_4| DL_8
		"""
		param = Conversions.enum_scalar_to_str(delta_length, enums.HrpUwbStsDeltaLen)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:STS:DLEN {param}')

	def get_key(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:HUWB:STS:KEY \n
		Snippet: value: List[str] = driver.source.bb.huwb.sts.get_key() \n
		Sets the key value of the scrambled timestamp sequence (STS) . The value is a 128-bit value in hexadecimal representation. \n
			:return: key: integer
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:STS:KEY?')
		return Conversions.str_to_str_list(response)

	def set_key(self, key: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:STS:KEY \n
		Snippet: driver.source.bb.huwb.sts.set_key(key = ['raw1', 'raw2', 'raw3']) \n
		Sets the key value of the scrambled timestamp sequence (STS) . The value is a 128-bit value in hexadecimal representation. \n
			:param key: integer
		"""
		param = Conversions.list_to_csv_str(key)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:STS:KEY {param}')

	# noinspection PyTypeChecker
	def get_pc(self) -> enums.HrpUwbStspAcketConfig:
		"""SCPI: [SOURce<HW>]:BB:HUWB:STS:PC \n
		Snippet: value: enums.HrpUwbStspAcketConfig = driver.source.bb.huwb.sts.get_pc() \n
		Sets the scrambled timestamp sequence (STS) packet configuration. \n
			:return: spc: SPC_0| SPC_1| SPC_2| SPC_3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:STS:PC?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbStspAcketConfig)

	def set_pc(self, spc: enums.HrpUwbStspAcketConfig) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:STS:PC \n
		Snippet: driver.source.bb.huwb.sts.set_pc(spc = enums.HrpUwbStspAcketConfig.SPC_0) \n
		Sets the scrambled timestamp sequence (STS) packet configuration. \n
			:param spc: SPC_0| SPC_1| SPC_2| SPC_3
		"""
		param = Conversions.enum_scalar_to_str(spc, enums.HrpUwbStspAcketConfig)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:STS:PC {param}')

	def get_upart(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:HUWB:STS:UPARt \n
		Snippet: value: List[str] = driver.source.bb.huwb.sts.get_upart() \n
		Sets the upper part of the V value. The value is a 96-bit value in hexadecimal representation. \n
			:return: upper_part: integer
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:STS:UPARt?')
		return Conversions.str_to_str_list(response)

	def set_upart(self, upper_part: List[str]) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:STS:UPARt \n
		Snippet: driver.source.bb.huwb.sts.set_upart(upper_part = ['raw1', 'raw2', 'raw3']) \n
		Sets the upper part of the V value. The value is a 96-bit value in hexadecimal representation. \n
			:param upper_part: integer
		"""
		param = Conversions.list_to_csv_str(upper_part)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:STS:UPARt {param}')
