from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Crate:
	"""Crate commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("crate", core, parent)

	def get_variation(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:C2K:CRATe:VARiation \n
		Snippet: value: float = driver.source.bb.c2K.crate.get_variation() \n
		Sets the output chip rate. The output chip rate changes the output clock and the modulation bandwidth, as well as the
		synchronization signals that are output. It does not affect the calculated chip sequence. \n
			:return: variation: float Range: 400 to 5E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:CRATe:VARiation?')
		return Conversions.str_to_float(response)

	def set_variation(self, variation: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:C2K:CRATe:VARiation \n
		Snippet: driver.source.bb.c2K.crate.set_variation(variation = 1.0) \n
		Sets the output chip rate. The output chip rate changes the output clock and the modulation bandwidth, as well as the
		synchronization signals that are output. It does not affect the calculated chip sequence. \n
			:param variation: float Range: 400 to 5E6
		"""
		param = Conversions.decimal_value_to_str(variation)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:CRATe:VARiation {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.Cdma2KchipRate:
		"""SCPI: [SOURce<HW>]:BB:C2K:CRATe \n
		Snippet: value: enums.Cdma2KchipRate = driver.source.bb.c2K.crate.get_value() \n
		The command queries the spreading rate. The output chip rate which determines the rate of the spread symbols as is used
		for signal output can be set with the command method RsSmbv.Source.Bb.C2K.Crate.variation. \n
			:return: crate: R1M2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:CRATe?')
		return Conversions.str_to_scalar_enum(response, enums.Cdma2KchipRate)
