from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Range:
	"""Range commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("range", core, parent)

	def get_down(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:RANGe:DOWN \n
		Snippet: value: float = driver.source.bb.w3Gpp.mstation.enhanced.dpdch.dpControl.range.get_down() \n
		The command selects the dynamic range for ranging up the channel power. \n
			:return: down: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:RANGe:DOWN?')
		return Conversions.str_to_float(response)

	def set_down(self, down: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:RANGe:DOWN \n
		Snippet: driver.source.bb.w3Gpp.mstation.enhanced.dpdch.dpControl.range.set_down(down = 1.0) \n
		The command selects the dynamic range for ranging up the channel power. \n
			:param down: float Range: 0 to 60, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(down)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:RANGe:DOWN {param}')

	def get_up(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:RANGe:UP \n
		Snippet: value: float = driver.source.bb.w3Gpp.mstation.enhanced.dpdch.dpControl.range.get_up() \n
		The command selects the dynamic range for ranging up the channel power. \n
			:return: up: float Range: 0 to 60, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:RANGe:UP?')
		return Conversions.str_to_float(response)

	def set_up(self, up: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:RANGe:UP \n
		Snippet: driver.source.bb.w3Gpp.mstation.enhanced.dpdch.dpControl.range.set_up(up = 1.0) \n
		The command selects the dynamic range for ranging up the channel power. \n
			:param up: float Range: 0 to 60, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(up)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:RANGe:UP {param}')
