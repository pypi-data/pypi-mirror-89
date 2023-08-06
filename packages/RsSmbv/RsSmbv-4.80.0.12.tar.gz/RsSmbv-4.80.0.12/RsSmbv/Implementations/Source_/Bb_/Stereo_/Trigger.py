from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trigger", core, parent)

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.TrigRunMode:
		"""SCPI: [SOURce<HW>]:BB:STEReo:TRIGger:RMODe \n
		Snippet: value: enums.TrigRunMode = driver.source.bb.stereo.trigger.get_rmode() \n
		No command help available \n
			:return: rm_ode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:TRIGger:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.TrigRunMode)

	def set_rmode(self, rm_ode: enums.TrigRunMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:STEReo:TRIGger:RMODe \n
		Snippet: driver.source.bb.stereo.trigger.set_rmode(rm_ode = enums.TrigRunMode.RUN) \n
		No command help available \n
			:param rm_ode: No help available
		"""
		param = Conversions.enum_scalar_to_str(rm_ode, enums.TrigRunMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:TRIGger:RMODe {param}')

	# noinspection PyTypeChecker
	def get_sequence(self) -> enums.FmStereoTrigMode:
		"""SCPI: [SOURce<HW>]:BB:STEReo:[TRIGger]:SEQuence \n
		Snippet: value: enums.FmStereoTrigMode = driver.source.bb.stereo.trigger.get_sequence() \n
		No command help available \n
			:return: sequence: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:TRIGger:SEQuence?')
		return Conversions.str_to_scalar_enum(response, enums.FmStereoTrigMode)

	def set_sequence(self, sequence: enums.FmStereoTrigMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:STEReo:[TRIGger]:SEQuence \n
		Snippet: driver.source.bb.stereo.trigger.set_sequence(sequence = enums.FmStereoTrigMode.AUTO) \n
		No command help available \n
			:param sequence: No help available
		"""
		param = Conversions.enum_scalar_to_str(sequence, enums.FmStereoTrigMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:TRIGger:SEQuence {param}')
