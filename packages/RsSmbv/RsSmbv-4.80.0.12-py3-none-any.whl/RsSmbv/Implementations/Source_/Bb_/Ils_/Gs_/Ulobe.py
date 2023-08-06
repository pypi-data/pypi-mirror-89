from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ulobe:
	"""Ulobe commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ulobe", core, parent)

	def get_frequency(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:ILS:[GS]:ULOBe:[FREQuency] \n
		Snippet: value: float = driver.source.bb.ils.gs.ulobe.get_frequency() \n
		Sets the modulation frequency of the antenna lobe arranged at the top viewed from the air plane for the ILS glide slope
		modulation signal. \n
			:return: frequency: float Range: 60 to 120
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:GS:ULOBe:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:ILS:[GS]:ULOBe:[FREQuency] \n
		Snippet: driver.source.bb.ils.gs.ulobe.set_frequency(frequency = 1.0) \n
		Sets the modulation frequency of the antenna lobe arranged at the top viewed from the air plane for the ILS glide slope
		modulation signal. \n
			:param frequency: float Range: 60 to 120
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:GS:ULOBe:FREQuency {param}')
