from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class External:
	"""External commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("external", core, parent)

	# noinspection PyTypeChecker
	def get_impedance(self) -> enums.InputImpRf:
		"""SCPI: [SOURce<HW>]:PULM:TRIGger:EXTernal:IMPedance \n
		Snippet: value: enums.InputImpRf = driver.source.pulm.trigger.external.get_impedance() \n
		No command help available \n
			:return: impedance: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:TRIGger:EXTernal:IMPedance?')
		return Conversions.str_to_scalar_enum(response, enums.InputImpRf)

	def set_impedance(self, impedance: enums.InputImpRf) -> None:
		"""SCPI: [SOURce<HW>]:PULM:TRIGger:EXTernal:IMPedance \n
		Snippet: driver.source.pulm.trigger.external.set_impedance(impedance = enums.InputImpRf.G10K) \n
		No command help available \n
			:param impedance: No help available
		"""
		param = Conversions.enum_scalar_to_str(impedance, enums.InputImpRf)
		self._core.io.write(f'SOURce<HwInstance>:PULM:TRIGger:EXTernal:IMPedance {param}')
