from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPy:
	"""FilterPy commands group definition. 17 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("filterPy", core, parent)

	@property
	def parameter(self):
		"""parameter commands group. 2 Sub-classes, 8 commands."""
		if not hasattr(self, '_parameter'):
			from .FilterPy_.Parameter import Parameter
			self._parameter = Parameter(self._core, self._base)
		return self._parameter

	def get_auto(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:FILTer:AUTO \n
		Snippet: value: bool = driver.source.bb.eutra.filterPy.get_auto() \n
		Queries if the internal ('Auto') filter is applied. This filter is selected automatically, if carrier aggregation with
		carriers that span different bandwidths is used. \n
			:return: auto: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:FILTer:AUTO?')
		return Conversions.str_to_bool(response)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.EutraFiltOptMode:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:FILTer:MODE \n
		Snippet: value: enums.EutraFiltOptMode = driver.source.bb.eutra.filterPy.get_mode() \n
		Selects an offline or real-time filter mode. \n
			:return: opt_mode: RTime| OFFLine
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:FILTer:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.EutraFiltOptMode)

	def set_mode(self, opt_mode: enums.EutraFiltOptMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:FILTer:MODE \n
		Snippet: driver.source.bb.eutra.filterPy.set_mode(opt_mode = enums.EutraFiltOptMode.OFFLine) \n
		Selects an offline or real-time filter mode. \n
			:param opt_mode: RTime| OFFLine
		"""
		param = Conversions.enum_scalar_to_str(opt_mode, enums.EutraFiltOptMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:FILTer:MODE {param}')

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.DmFilterEutra:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:FILTer:TYPE \n
		Snippet: value: enums.DmFilterEutra = driver.source.bb.eutra.filterPy.get_type_py() \n
		Selects the baseband filter type. \n
			:return: type_py: RCOSine| COSine| GAUSs| LGAuss| CONE| COF705| COEQualizer| COFequalizer| C2K3x| RECTangle| PGAuss| LPASs| DIRac| ENPShape| EWPShape| LTEFilter| LPASSEVM| SPHase| APCO25| USER
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:FILTer:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.DmFilterEutra)

	def set_type_py(self, type_py: enums.DmFilterEutra) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:FILTer:TYPE \n
		Snippet: driver.source.bb.eutra.filterPy.set_type_py(type_py = enums.DmFilterEutra.APCO25) \n
		Selects the baseband filter type. \n
			:param type_py: RCOSine| COSine| GAUSs| LGAuss| CONE| COF705| COEQualizer| COFequalizer| C2K3x| RECTangle| PGAuss| LPASs| DIRac| ENPShape| EWPShape| LTEFilter| LPASSEVM| SPHase| APCO25| USER
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.DmFilterEutra)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:FILTer:TYPE {param}')

	def clone(self) -> 'FilterPy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FilterPy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
