from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ramp:
	"""Ramp commands group definition. 21 total commands, 5 Sub-groups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ramp", core, parent)

	@property
	def blank(self):
		"""blank commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_blank'):
			from .Ramp_.Blank import Blank
			self._blank = Blank(self._core, self._base)
		return self._blank

	@property
	def fall(self):
		"""fall commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fall'):
			from .Ramp_.Fall import Fall
			self._fall = Fall(self._core, self._base)
		return self._fall

	@property
	def preSweep(self):
		"""preSweep commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_preSweep'):
			from .Ramp_.PreSweep import PreSweep
			self._preSweep = PreSweep(self._core, self._base)
		return self._preSweep

	@property
	def stair(self):
		"""stair commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_stair'):
			from .Ramp_.Stair import Stair
			self._stair = Stair(self._core, self._base)
		return self._stair

	@property
	def sweep(self):
		"""sweep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sweep'):
			from .Ramp_.Sweep import Sweep
			self._sweep = Sweep(self._core, self._base)
		return self._sweep

	def get_attenuation(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:ATTenuation \n
		Snippet: value: float = driver.source.bb.pramp.ramp.get_attenuation() \n
		No command help available \n
			:return: const_atten: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:ATTenuation?')
		return Conversions.str_to_float(response)

	def set_attenuation(self, const_atten: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:ATTenuation \n
		Snippet: driver.source.bb.pramp.ramp.set_attenuation(const_atten = 1.0) \n
		No command help available \n
			:param const_atten: No help available
		"""
		param = Conversions.decimal_value_to_str(const_atten)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:RAMP:ATTenuation {param}')

	def get_constmode(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:CONStmode \n
		Snippet: value: bool = driver.source.bb.pramp.ramp.get_constmode() \n
		No command help available \n
			:return: const_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:CONStmode?')
		return Conversions.str_to_bool(response)

	def set_constmode(self, const_mode: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:CONStmode \n
		Snippet: driver.source.bb.pramp.ramp.set_constmode(const_mode = False) \n
		No command help available \n
			:param const_mode: No help available
		"""
		param = Conversions.bool_to_str(const_mode)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:RAMP:CONStmode {param}')

	def get_level(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:LEVel \n
		Snippet: value: float = driver.source.bb.pramp.ramp.get_level() \n
		No command help available \n
			:return: const_level: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:LEVel?')
		return Conversions.str_to_float(response)

	def get_range(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:RANGe \n
		Snippet: value: float = driver.source.bb.pramp.ramp.get_range() \n
		No command help available \n
			:return: range_py: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:RANGe?')
		return Conversions.str_to_float(response)

	def set_range(self, range_py: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:RANGe \n
		Snippet: driver.source.bb.pramp.ramp.set_range(range_py = 1.0) \n
		No command help available \n
			:param range_py: No help available
		"""
		param = Conversions.decimal_value_to_str(range_py)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:RAMP:RANGe {param}')

	def get_resolution(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:RESolution \n
		Snippet: value: float = driver.source.bb.pramp.ramp.get_resolution() \n
		No command help available \n
			:return: power_resolution: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:RESolution?')
		return Conversions.str_to_float(response)

	def get_sample_rate(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:SAMPlerate \n
		Snippet: value: float = driver.source.bb.pramp.ramp.get_sample_rate() \n
		No command help available \n
			:return: sample_rate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:SAMPlerate?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_shape(self) -> enums.PowerRampShape:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:SHAPe \n
		Snippet: value: enums.PowerRampShape = driver.source.bb.pramp.ramp.get_shape() \n
		No command help available \n
			:return: shape: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:SHAPe?')
		return Conversions.str_to_scalar_enum(response, enums.PowerRampShape)

	def set_shape(self, shape: enums.PowerRampShape) -> None:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:SHAPe \n
		Snippet: driver.source.bb.pramp.ramp.set_shape(shape = enums.PowerRampShape.LINear) \n
		No command help available \n
			:param shape: No help available
		"""
		param = Conversions.enum_scalar_to_str(shape, enums.PowerRampShape)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:RAMP:SHAPe {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.PowerRampSlope:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:SLOPe \n
		Snippet: value: enums.PowerRampSlope = driver.source.bb.pramp.ramp.get_slope() \n
		No command help available \n
			:return: slope: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.PowerRampSlope)

	def set_slope(self, slope: enums.PowerRampSlope) -> None:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:SLOPe \n
		Snippet: driver.source.bb.pramp.ramp.set_slope(slope = enums.PowerRampSlope.ASCending) \n
		No command help available \n
			:param slope: No help available
		"""
		param = Conversions.enum_scalar_to_str(slope, enums.PowerRampSlope)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:RAMP:SLOPe {param}')

	def get_start_level(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:STARtlevel \n
		Snippet: value: float = driver.source.bb.pramp.ramp.get_start_level() \n
		No command help available \n
			:return: start_level: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:STARtlevel?')
		return Conversions.str_to_float(response)

	def get_stop_level(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:PRAMp:RAMP:STOPlevel \n
		Snippet: value: float = driver.source.bb.pramp.ramp.get_stop_level() \n
		No command help available \n
			:return: stop_level: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:STOPlevel?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Ramp':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ramp(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
