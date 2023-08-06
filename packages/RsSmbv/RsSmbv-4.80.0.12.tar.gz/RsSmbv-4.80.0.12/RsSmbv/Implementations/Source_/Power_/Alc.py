from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Alc:
	"""Alc commands group definition. 7 total commands, 1 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("alc", core, parent)

	@property
	def sonce(self):
		"""sonce commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sonce'):
			from .Alc_.Sonce import Sonce
			self._sonce = Sonce(self._core, self._base)
		return self._sonce

	# noinspection PyTypeChecker
	def get_dsensitivity(self) -> enums.PowAlcDetSensitivity:
		"""SCPI: [SOURce<HW>]:POWer:ALC:DSENsitivity \n
		Snippet: value: enums.PowAlcDetSensitivity = driver.source.power.alc.get_dsensitivity() \n
		Sets the sensitivity of the ALC detector. \n
			:return: sensitivity: AUTO| FIXed AUTO Selects the optimum sensitivity automatically. FIXed Fixes the internal level detector.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ALC:DSENsitivity?')
		return Conversions.str_to_scalar_enum(response, enums.PowAlcDetSensitivity)

	def set_dsensitivity(self, sensitivity: enums.PowAlcDetSensitivity) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ALC:DSENsitivity \n
		Snippet: driver.source.power.alc.set_dsensitivity(sensitivity = enums.PowAlcDetSensitivity.AUTO) \n
		Sets the sensitivity of the ALC detector. \n
			:param sensitivity: AUTO| FIXed AUTO Selects the optimum sensitivity automatically. FIXed Fixes the internal level detector.
		"""
		param = Conversions.enum_scalar_to_str(sensitivity, enums.PowAlcDetSensitivity)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ALC:DSENsitivity {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AlcOnOffAuto:
		"""SCPI: [SOURce<HW>]:POWer:ALC:MODE \n
		Snippet: value: enums.AlcOnOffAuto = driver.source.power.alc.get_mode() \n
		Queries the currently set ALC mode. See method RsSmbv.Source.Power.Level.Immediate.amplitude. \n
			:return: pow_alc_mode: 0| AUTO| 1| PRESet| OFFTable| ON| OFF| ONSample| ONTable
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ALC:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AlcOnOffAuto)

	# noinspection PyTypeChecker
	def get_omode(self) -> enums.AlcOffModeSmbv:
		"""SCPI: [SOURce<HW>]:POWer:ALC:OMODe \n
		Snippet: value: enums.AlcOffModeSmbv = driver.source.power.alc.get_omode() \n
		No command help available \n
			:return: off_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ALC:OMODe?')
		return Conversions.str_to_scalar_enum(response, enums.AlcOffModeSmbv)

	def set_omode(self, off_mode: enums.AlcOffModeSmbv) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ALC:OMODe \n
		Snippet: driver.source.power.alc.set_omode(off_mode = enums.AlcOffModeSmbv.HIGHaccuracy) \n
		No command help available \n
			:param off_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(off_mode, enums.AlcOffModeSmbv)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ALC:OMODe {param}')

	def get_search(self) -> bool:
		"""SCPI: [SOURce<HW>]:POWer:ALC:SEARch \n
		Snippet: value: bool = driver.source.power.alc.get_search() \n
		No command help available \n
			:return: search: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ALC:SEARch?')
		return Conversions.str_to_bool(response)

	def set_search(self, search: bool) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ALC:SEARch \n
		Snippet: driver.source.power.alc.set_search(search = False) \n
		No command help available \n
			:param search: No help available
		"""
		param = Conversions.bool_to_str(search)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ALC:SEARch {param}')

	# noinspection PyTypeChecker
	def get_slevel(self) -> enums.PowAlcSampleLev:
		"""SCPI: [SOURce<HW>]:POWer:ALC:SLEVel \n
		Snippet: value: enums.PowAlcSampleLev = driver.source.power.alc.get_slevel() \n
		Sets the sample level of automatic level control (ALC) . How To: See 'How to Enable the ALC'. \n
			:return: samp_level: FULL| MINimum| ATTenuated
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ALC:SLEVel?')
		return Conversions.str_to_scalar_enum(response, enums.PowAlcSampleLev)

	def set_slevel(self, samp_level: enums.PowAlcSampleLev) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ALC:SLEVel \n
		Snippet: driver.source.power.alc.set_slevel(samp_level = enums.PowAlcSampleLev.ATTenuated) \n
		Sets the sample level of automatic level control (ALC) . How To: See 'How to Enable the ALC'. \n
			:param samp_level: FULL| MINimum| ATTenuated
		"""
		param = Conversions.enum_scalar_to_str(samp_level, enums.PowAlcSampleLev)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ALC:SLEVel {param}')

	# noinspection PyTypeChecker
	def get_state(self) -> enums.AlcOnOffAuto:
		"""SCPI: [SOURce<HW>]:POWer:ALC:[STATe] \n
		Snippet: value: enums.AlcOnOffAuto = driver.source.power.alc.get_state() \n
		Activates automatic level control in the selected mode. How to: See 'How to Enable the ALC'. \n
			:return: state: AUTO| OFFTable| ON| ONSample| ONTable| OFF AUTO Adjusts the output level to the operating conditions automatically. OFFTable Controls the level with the attenuation values of the internal ALC table. ON Activates internal level control permanently. OFF Deactivates internal level control, 'Sample & Hold' mode is active. ONSample Starts the internal level control with the first change. ONTable Starts with the attenuation setting from the table and continues with automatic level control. For more details on the individual settings, an overview of the functionality and details on what is to be considered, see 'ALC states and their effects'.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ALC:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.AlcOnOffAuto)

	def set_state(self, state: enums.AlcOnOffAuto) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ALC:[STATe] \n
		Snippet: driver.source.power.alc.set_state(state = enums.AlcOnOffAuto._0) \n
		Activates automatic level control in the selected mode. How to: See 'How to Enable the ALC'. \n
			:param state: AUTO| OFFTable| ON| ONSample| ONTable| OFF AUTO Adjusts the output level to the operating conditions automatically. OFFTable Controls the level with the attenuation values of the internal ALC table. ON Activates internal level control permanently. OFF Deactivates internal level control, 'Sample & Hold' mode is active. ONSample Starts the internal level control with the first change. ONTable Starts with the attenuation setting from the table and continues with automatic level control. For more details on the individual settings, an overview of the functionality and details on what is to be considered, see 'ALC states and their effects'.
		"""
		param = Conversions.enum_scalar_to_str(state, enums.AlcOnOffAuto)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ALC:STATe {param}')

	def clone(self) -> 'Alc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Alc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
