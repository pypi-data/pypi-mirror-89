from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Alevel:
	"""Alevel commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("alevel", core, parent)

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:ALEVel:VALue \n
		Snippet: value: float = driver.source.correction.fresponse.rf.user.alevel.get_value() \n
		If method RsSmbv.Source.Correction.Fresponse.Rf.User.state1, queries the absolute level correction value. \n
			:return: freq_cor_rf_absolute_val: float Range: -100 to 100, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:USER:ALEVel:VALue?')
		return Conversions.str_to_float(response)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:ALEVel:[STATe] \n
		Snippet: value: bool = driver.source.correction.fresponse.rf.user.alevel.get_state() \n
		Activates absolute level compensation at the current center frequency. Query the level correction value with the command
		method RsSmbv.Source.Correction.Fresponse.Rf.User.Alevel.value. \n
			:return: freq_corr_rf_al_sta: 0| 1| OFF| ON Absolute level compensation and user correction cannot be activated simultaneously. These functions exclude each other; only one of them can be used at a time. .
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:USER:ALEVel:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, freq_corr_rf_al_sta: bool) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:ALEVel:[STATe] \n
		Snippet: driver.source.correction.fresponse.rf.user.alevel.set_state(freq_corr_rf_al_sta = False) \n
		Activates absolute level compensation at the current center frequency. Query the level correction value with the command
		method RsSmbv.Source.Correction.Fresponse.Rf.User.Alevel.value. \n
			:param freq_corr_rf_al_sta: 0| 1| OFF| ON Absolute level compensation and user correction cannot be activated simultaneously. These functions exclude each other; only one of them can be used at a time. .
		"""
		param = Conversions.bool_to_str(freq_corr_rf_al_sta)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:ALEVel:STATe {param}')
