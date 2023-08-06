from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Id:
	"""Id commands group definition. 14 total commands, 2 Sub-groups, 11 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("id", core, parent)

	@property
	def code(self):
		"""code commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_code'):
			from .Id_.Code import Code
			self._code = Code(self._core, self._base)
		return self._code

	@property
	def ppp(self):
		"""ppp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ppp'):
			from .Id_.Ppp import Ppp
			self._ppp = Ppp(self._core, self._base)
		return self._ppp

	def get_dash(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:DASH \n
		Snippet: value: float = driver.source.bb.dme.id.get_dash() \n
		Sets the length of a Morse code dash. Available only if method RsSmbv.Source.Bb.Dme.Id.tschema is set to USER. \n
			:return: dash: float Range: 0.05 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ID:DASH?')
		return Conversions.str_to_float(response)

	def set_dash(self, dash: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:DASH \n
		Snippet: driver.source.bb.dme.id.set_dash(dash = 1.0) \n
		Sets the length of a Morse code dash. Available only if method RsSmbv.Source.Bb.Dme.Id.tschema is set to USER. \n
			:param dash: float Range: 0.05 to 1
		"""
		param = Conversions.decimal_value_to_str(dash)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ID:DASH {param}')

	def get_dot(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:DOT \n
		Snippet: value: float = driver.source.bb.dme.id.get_dot() \n
		Sets the length of a Morse code dot. \n
			:return: dot: float Range: 0.05 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ID:DOT?')
		return Conversions.str_to_float(response)

	def set_dot(self, dot: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:DOT \n
		Snippet: driver.source.bb.dme.id.set_dot(dot = 1.0) \n
		Sets the length of a Morse code dot. \n
			:param dot: float Range: 0.05 to 1
		"""
		param = Conversions.decimal_value_to_str(dot)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ID:DOT {param}')

	def get_dot_length(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:DOTLength \n
		Snippet: value: float = driver.source.bb.dme.id.get_dot_length() \n
		No command help available \n
			:return: dotlength: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ID:DOTLength?')
		return Conversions.str_to_float(response)

	def set_dot_length(self, dotlength: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:DOTLength \n
		Snippet: driver.source.bb.dme.id.set_dot_length(dotlength = 1.0) \n
		No command help available \n
			:param dotlength: No help available
		"""
		param = Conversions.decimal_value_to_str(dotlength)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ID:DOTLength {param}')

	def get_letter(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:LETTer \n
		Snippet: value: float = driver.source.bb.dme.id.get_letter() \n
		Sets the length of a Morse code letter space. Available only if method RsSmbv.Source.Bb.Dme.Id.tschema is set to USER. \n
			:return: letter: float Range: 0.05 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ID:LETTer?')
		return Conversions.str_to_float(response)

	def set_letter(self, letter: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:LETTer \n
		Snippet: driver.source.bb.dme.id.set_letter(letter = 1.0) \n
		Sets the length of a Morse code letter space. Available only if method RsSmbv.Source.Bb.Dme.Id.tschema is set to USER. \n
			:param letter: float Range: 0.05 to 1
		"""
		param = Conversions.decimal_value_to_str(letter)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ID:LETTer {param}')

	def get_period(self) -> int:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:PERiod \n
		Snippet: value: int = driver.source.bb.dme.id.get_period() \n
		Sets the period of the COM/ID signal. \n
			:return: period: integer Range: 10 to 120
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ID:PERiod?')
		return Conversions.str_to_int(response)

	def set_period(self, period: int) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:PERiod \n
		Snippet: driver.source.bb.dme.id.set_period(period = 1) \n
		Sets the period of the COM/ID signal. \n
			:param period: integer Range: 10 to 120
		"""
		param = Conversions.decimal_value_to_str(period)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ID:PERiod {param}')

	def get_pps(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:PPS \n
		Snippet: value: float = driver.source.bb.dme.id.get_pps() \n
		Sets the morse pulse pair spacing. \n
			:return: pulse_pair_spacin: float Range: 2E-6 to 300E-6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ID:PPS?')
		return Conversions.str_to_float(response)

	def set_pps(self, pulse_pair_spacin: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:PPS \n
		Snippet: driver.source.bb.dme.id.set_pps(pulse_pair_spacin = 1.0) \n
		Sets the morse pulse pair spacing. \n
			:param pulse_pair_spacin: float Range: 2E-6 to 300E-6
		"""
		param = Conversions.decimal_value_to_str(pulse_pair_spacin)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ID:PPS {param}')

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:PRESet \n
		Snippet: driver.source.bb.dme.id.preset() \n
		Sets the default settings for the ID signal. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ID:PRESet')

	def preset_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:PRESet \n
		Snippet: driver.source.bb.dme.id.preset_with_opc() \n
		Sets the default settings for the ID signal. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:DME:ID:PRESet')

	def get_rate(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:RATE \n
		Snippet: value: float = driver.source.bb.dme.id.get_rate() \n
		Sets the pulse repetition rate of the ID sequence. \n
			:return: rate: float Range: 100 to 10E3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ID:RATE?')
		return Conversions.str_to_float(response)

	def set_rate(self, rate: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:RATE \n
		Snippet: driver.source.bb.dme.id.set_rate(rate = 1.0) \n
		Sets the pulse repetition rate of the ID sequence. \n
			:param rate: float Range: 100 to 10E3
		"""
		param = Conversions.decimal_value_to_str(rate)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ID:RATE {param}')

	def get_symbol(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:SYMBol \n
		Snippet: value: float = driver.source.bb.dme.id.get_symbol() \n
		Sets the length of the Morse code symbol space. Available only if method RsSmbv.Source.Bb.Dme.Id.tschema is set to USER. \n
			:return: symbol: float Range: 0.05 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ID:SYMBol?')
		return Conversions.str_to_float(response)

	def set_symbol(self, symbol: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:SYMBol \n
		Snippet: driver.source.bb.dme.id.set_symbol(symbol = 1.0) \n
		Sets the length of the Morse code symbol space. Available only if method RsSmbv.Source.Bb.Dme.Id.tschema is set to USER. \n
			:param symbol: float Range: 0.05 to 1
		"""
		param = Conversions.decimal_value_to_str(symbol)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ID:SYMBol {param}')

	# noinspection PyTypeChecker
	def get_tschema(self) -> enums.AvionicComIdTimeSchem:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:TSCHema \n
		Snippet: value: enums.AvionicComIdTimeSchem = driver.source.bb.dme.id.get_tschema() \n
		Sets the time schema of the Morse code for the COM/ID signal. \n
			:return: tschema: STD| USER
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ID:TSCHema?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicComIdTimeSchem)

	def set_tschema(self, tschema: enums.AvionicComIdTimeSchem) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:TSCHema \n
		Snippet: driver.source.bb.dme.id.set_tschema(tschema = enums.AvionicComIdTimeSchem.STD) \n
		Sets the time schema of the Morse code for the COM/ID signal. \n
			:param tschema: STD| USER
		"""
		param = Conversions.enum_scalar_to_str(tschema, enums.AvionicComIdTimeSchem)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ID:TSCHema {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:[STATe] \n
		Snippet: value: bool = driver.source.bb.dme.id.get_state() \n
		Enables/disables the COM/ID signal. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ID:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:ID:[STATe] \n
		Snippet: driver.source.bb.dme.id.set_state(state = False) \n
		Enables/disables the COM/ID signal. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ID:STATe {param}')

	def clone(self) -> 'Id':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Id(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
