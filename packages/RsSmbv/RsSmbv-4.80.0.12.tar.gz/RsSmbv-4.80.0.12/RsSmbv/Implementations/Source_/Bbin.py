from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bbin:
	"""Bbin commands group definition. 30 total commands, 7 Sub-groups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bbin", core, parent)

	@property
	def alevel(self):
		"""alevel commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_alevel'):
			from .Bbin_.Alevel import Alevel
			self._alevel = Alevel(self._core, self._base)
		return self._alevel

	@property
	def channel(self):
		"""channel commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_channel'):
			from .Bbin_.Channel import Channel
			self._channel = Channel(self._core, self._base)
		return self._channel

	@property
	def digital(self):
		"""digital commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_digital'):
			from .Bbin_.Digital import Digital
			self._digital = Digital(self._core, self._base)
		return self._digital

	@property
	def iqswap(self):
		"""iqswap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqswap'):
			from .Bbin_.Iqswap import Iqswap
			self._iqswap = Iqswap(self._core, self._base)
		return self._iqswap

	@property
	def oload(self):
		"""oload commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_oload'):
			from .Bbin_.Oload import Oload
			self._oload = Oload(self._core, self._base)
		return self._oload

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_power'):
			from .Bbin_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Bbin_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	def get_cdevice(self) -> str:
		"""SCPI: [SOURce<HW>]:BBIN:CDEVice \n
		Snippet: value: str = driver.source.bbin.get_cdevice() \n
		Indicates the ID of an externally connected Rohde & Schwarz Instrument or Rohde & Schwarz device. \n
			:return: cdevice: string 'None' - no device is connected.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:CDEVice?')
		return trim_str_response(response)

	def get_cfactor(self) -> float:
		"""SCPI: [SOURce<HW>]:BBIN:CFACtor \n
		Snippet: value: float = driver.source.bbin.get_cfactor() \n
		No command help available \n
			:return: cfactor: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:CFACtor?')
		return Conversions.str_to_float(response)

	def set_cfactor(self, cfactor: float) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:CFACtor \n
		Snippet: driver.source.bbin.set_cfactor(cfactor = 1.0) \n
		No command help available \n
			:param cfactor: No help available
		"""
		param = Conversions.decimal_value_to_str(cfactor)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:CFACtor {param}')

	def get_foffset(self) -> float:
		"""SCPI: [SOURce<HW>]:BBIN:FOFFset \n
		Snippet: value: float = driver.source.bbin.get_foffset() \n
		Sets a frequency offset for the internal/external baseband signal. The offset affects the generated baseband signal. \n
			:return: fo_ffset: float Range: depends on the installed options , Unit: Hz E.g. -60 MHz to +60 MHz (base unit)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:FOFFset?')
		return Conversions.str_to_float(response)

	def set_foffset(self, fo_ffset: float) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:FOFFset \n
		Snippet: driver.source.bbin.set_foffset(fo_ffset = 1.0) \n
		Sets a frequency offset for the internal/external baseband signal. The offset affects the generated baseband signal. \n
			:param fo_ffset: float Range: depends on the installed options , Unit: Hz E.g. -60 MHz to +60 MHz (base unit)
		"""
		param = Conversions.decimal_value_to_str(fo_ffset)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:FOFFset {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.BbinModeDigital:
		"""SCPI: [SOURce<HW>]:BBIN:MODE \n
		Snippet: value: enums.BbinModeDigital = driver.source.bbin.get_mode() \n
		Defines that a digital external signal is applied. \n
			:return: mode: DIGital
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.BbinModeDigital)

	def set_mode(self, mode: enums.BbinModeDigital) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:MODE \n
		Snippet: driver.source.bbin.set_mode(mode = enums.BbinModeDigital.DIGital) \n
		Defines that a digital external signal is applied. \n
			:param mode: DIGital
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.BbinModeDigital)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:MODE {param}')

	def get_mperiod(self) -> int:
		"""SCPI: [SOURce<HW>]:BBIN:MPERiod \n
		Snippet: value: int = driver.source.bbin.get_mperiod() \n
		Sets the recording duration for measuring the baseband input signal by executed method RsSmbv.Source.Bbin.Alevel.Execute.
		set. \n
			:return: mp_eriod: integer Range: 1 to 32, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:MPERiod?')
		return Conversions.str_to_int(response)

	def set_mperiod(self, mp_eriod: int) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:MPERiod \n
		Snippet: driver.source.bbin.set_mperiod(mp_eriod = 1) \n
		Sets the recording duration for measuring the baseband input signal by executed method RsSmbv.Source.Bbin.Alevel.Execute.
		set. \n
			:param mp_eriod: integer Range: 1 to 32, Unit: s
		"""
		param = Conversions.decimal_value_to_str(mp_eriod)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:MPERiod {param}')

	def get_pgain(self) -> float:
		"""SCPI: [SOURce<HW>]:BBIN:PGAin \n
		Snippet: value: float = driver.source.bbin.get_pgain() \n
		No command help available \n
			:return: pgain: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:PGAin?')
		return Conversions.str_to_float(response)

	def set_pgain(self, pgain: float) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:PGAin \n
		Snippet: driver.source.bbin.set_pgain(pgain = 1.0) \n
		No command help available \n
			:param pgain: No help available
		"""
		param = Conversions.decimal_value_to_str(pgain)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:PGAin {param}')

	def get_poffset(self) -> float:
		"""SCPI: [SOURce<HW>]:BBIN:POFFset \n
		Snippet: value: float = driver.source.bbin.get_poffset() \n
		Sets the relative phase offset for the external baseband signal. \n
			:return: poffset: float Range: -999.99 to 999.99, Unit: DEG
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:POFFset?')
		return Conversions.str_to_float(response)

	def set_poffset(self, poffset: float) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:POFFset \n
		Snippet: driver.source.bbin.set_poffset(poffset = 1.0) \n
		Sets the relative phase offset for the external baseband signal. \n
			:param poffset: float Range: -999.99 to 999.99, Unit: DEG
		"""
		param = Conversions.decimal_value_to_str(poffset)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:POFFset {param}')

	# noinspection PyTypeChecker
	def get_route(self) -> enums.PathUniCodBbin:
		"""SCPI: [SOURce<HW>]:BBIN:ROUTe \n
		Snippet: value: enums.PathUniCodBbin = driver.source.bbin.get_route() \n
		Selects the signal route for the internal/external baseband signal. \n
			:return: route: A
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:ROUTe?')
		return Conversions.str_to_scalar_enum(response, enums.PathUniCodBbin)

	def set_route(self, route: enums.PathUniCodBbin) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:ROUTe \n
		Snippet: driver.source.bbin.set_route(route = enums.PathUniCodBbin.A) \n
		Selects the signal route for the internal/external baseband signal. \n
			:param route: A
		"""
		param = Conversions.enum_scalar_to_str(route, enums.PathUniCodBbin)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:ROUTe {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BBIN:STATe \n
		Snippet: value: bool = driver.source.bbin.get_state() \n
		Switches the feeding of an external analog signal into the signal path on/off. Note: Interdependencies
			INTRO_CMD_HELP: The following functions cannot be activated simultaneously. They deactivate each other. \n
			- The internal baseband generator ([:SOURce<hw>]:BB:<DigStd>:STATe) and the external digital baseband input ([:SOURce<hw>]:BBIN:STATe)
			- The external digital baseband input ([:SOURce<hw>]:BBIN:STATe) and digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) because they share the same physical connectors (Dig I/Q and the HS Dig I/Q) .
			- The digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) and the output of analog I/Q signals:
			Table Header:  \n
			- If [:SOURce<hw>]:IQ:SOURce BASeband, [:SOURce<hw>]:IQ:STATe + method RsSmbv.Output.State.value or
			- [:SOURce<hw>]:IQ:OUTPut:ANALog:STATe \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:STATe \n
		Snippet: driver.source.bbin.set_state(state = False) \n
		Switches the feeding of an external analog signal into the signal path on/off. Note: Interdependencies
			INTRO_CMD_HELP: The following functions cannot be activated simultaneously. They deactivate each other. \n
			- The internal baseband generator ([:SOURce<hw>]:BB:<DigStd>:STATe) and the external digital baseband input ([:SOURce<hw>]:BBIN:STATe)
			- The external digital baseband input ([:SOURce<hw>]:BBIN:STATe) and digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) because they share the same physical connectors (Dig I/Q and the HS Dig I/Q) .
			- The digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) and the output of analog I/Q signals:
			Table Header:  \n
			- If [:SOURce<hw>]:IQ:SOURce BASeband, [:SOURce<hw>]:IQ:STATe + method RsSmbv.Output.State.value or
			- [:SOURce<hw>]:IQ:OUTPut:ANALog:STATe \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:STATe {param}')

	def clone(self) -> 'Bbin':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bbin(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
