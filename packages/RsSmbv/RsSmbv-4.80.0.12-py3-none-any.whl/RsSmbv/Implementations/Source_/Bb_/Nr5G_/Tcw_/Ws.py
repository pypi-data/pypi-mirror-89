from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ws:
	"""Ws commands group definition. 26 total commands, 5 Sub-groups, 17 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ws", core, parent)

	@property
	def adMrs(self):
		"""adMrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adMrs'):
			from .Ws_.AdMrs import AdMrs
			self._adMrs = AdMrs(self._core, self._base)
		return self._adMrs

	@property
	def frc(self):
		"""frc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frc'):
			from .Ws_.Frc import Frc
			self._frc = Frc(self._core, self._base)
		return self._frc

	@property
	def prach(self):
		"""prach commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_prach'):
			from .Ws_.Prach import Prach
			self._prach = Prach(self._core, self._base)
		return self._prach

	@property
	def ptrs(self):
		"""ptrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptrs'):
			from .Ws_.Ptrs import Ptrs
			self._ptrs = Ptrs(self._core, self._base)
		return self._ptrs

	@property
	def uci(self):
		"""uci commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_uci'):
			from .Ws_.Uci import Uci
			self._uci = Uci(self._core, self._base)
		return self._uci

	# noinspection PyTypeChecker
	def get_cbw(self) -> enums.Nr5Gcbw:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:CBW \n
		Snippet: value: enums.Nr5Gcbw = driver.source.bb.nr5G.tcw.ws.get_cbw() \n
		Selects the channel bandwidth. \n
			:return: ws_ch_bw: BW5| BW10| BW15| BW20| BW25| BW40| BW50| BW60| BW100| BW80| BW400| BW200| BW30| BW70| BW90 Bandwidth in MHz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:CBW?')
		return Conversions.str_to_scalar_enum(response, enums.Nr5Gcbw)

	def set_cbw(self, ws_ch_bw: enums.Nr5Gcbw) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:CBW \n
		Snippet: driver.source.bb.nr5G.tcw.ws.set_cbw(ws_ch_bw = enums.Nr5Gcbw.BW10) \n
		Selects the channel bandwidth. \n
			:param ws_ch_bw: BW5| BW10| BW15| BW20| BW25| BW40| BW50| BW60| BW100| BW80| BW400| BW200| BW30| BW70| BW90 Bandwidth in MHz
		"""
		param = Conversions.enum_scalar_to_str(ws_ch_bw, enums.Nr5Gcbw)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:CBW {param}')

	def get_cellid(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:CELLid \n
		Snippet: value: int = driver.source.bb.nr5G.tcw.ws.get_cellid() \n
		Sets the cell ID. \n
			:return: ws_cell_id: integer Range: 0 to 1007
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:CELLid?')
		return Conversions.str_to_int(response)

	def set_cellid(self, ws_cell_id: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:CELLid \n
		Snippet: driver.source.bb.nr5G.tcw.ws.set_cellid(ws_cell_id = 1) \n
		Sets the cell ID. \n
			:param ws_cell_id: integer Range: 0 to 1007
		"""
		param = Conversions.decimal_value_to_str(ws_cell_id)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:CELLid {param}')

	# noinspection PyTypeChecker
	def get_duplex(self) -> enums.EutraDuplexMode:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:DUPLex \n
		Snippet: value: enums.EutraDuplexMode = driver.source.bb.nr5G.tcw.ws.get_duplex() \n
		The duplexing mechanism used can be switched between FDD and TDD. \n
			:return: duplexing: FDD| TDD
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:DUPLex?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDuplexMode)

	def set_duplex(self, duplexing: enums.EutraDuplexMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:DUPLex \n
		Snippet: driver.source.bb.nr5G.tcw.ws.set_duplex(duplexing = enums.EutraDuplexMode.FDD) \n
		The duplexing mechanism used can be switched between FDD and TDD. \n
			:param duplexing: FDD| TDD
		"""
		param = Conversions.enum_scalar_to_str(duplexing, enums.EutraDuplexMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:DUPLex {param}')

	# noinspection PyTypeChecker
	def get_fm_throughput(self) -> enums.Fmt:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:FMTHroughput \n
		Snippet: value: enums.Fmt = driver.source.bb.nr5G.tcw.ws.get_fm_throughput() \n
		The required throughput is expressed as a fraction of maximum throughput for the FRC. The performance requirements assume
		HARQ retransmissions. The throughput shall be equal to or larger than the fraction of maximum throughput for the FRCs at
		the given SNR. \n
			:return: fmt: FMT70
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:FMTHroughput?')
		return Conversions.str_to_scalar_enum(response, enums.Fmt)

	# noinspection PyTypeChecker
	def get_fr_offset(self) -> enums.FreqOffset:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:FROFfset \n
		Snippet: value: enums.FreqOffset = driver.source.bb.nr5G.tcw.ws.get_fr_offset() \n
		Sets the frequency offset used for the PRACH. \n
			:return: freq_offset: FO_0| FO_400
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:FROFfset?')
		return Conversions.str_to_scalar_enum(response, enums.FreqOffset)

	def set_fr_offset(self, freq_offset: enums.FreqOffset) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:FROFfset \n
		Snippet: driver.source.bb.nr5G.tcw.ws.set_fr_offset(freq_offset = enums.FreqOffset.FO_0) \n
		Sets the frequency offset used for the PRACH. \n
			:param freq_offset: FO_0| FO_400
		"""
		param = Conversions.enum_scalar_to_str(freq_offset, enums.FreqOffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:FROFfset {param}')

	# noinspection PyTypeChecker
	def get_map_type(self) -> enums.MappingType:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:MAPType \n
		Snippet: value: enums.MappingType = driver.source.bb.nr5G.tcw.ws.get_map_type() \n
		Sets the mapping type A or B for the PUSCH. \n
			:return: map_type: A| B
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:MAPType?')
		return Conversions.str_to_scalar_enum(response, enums.MappingType)

	def set_map_type(self, map_type: enums.MappingType) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:MAPType \n
		Snippet: driver.source.bb.nr5G.tcw.ws.set_map_type(map_type = enums.MappingType.A) \n
		Sets the mapping type A or B for the PUSCH. \n
			:param map_type: A| B
		"""
		param = Conversions.enum_scalar_to_str(map_type, enums.MappingType)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:MAPType {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.Mode:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:MODE \n
		Snippet: value: enums.Mode = driver.source.bb.nr5G.tcw.ws.get_mode() \n
		Switches between the detection rate (Pd) and the false detection rate (Pfa) . \n
			:return: mode: DRAT| FDR DRAT Pd is defined as the probability of detection of preamble. FDR Pfa is defined as the total probability of false detection of the preamble.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.Mode)

	def set_mode(self, mode: enums.Mode) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:MODE \n
		Snippet: driver.source.bb.nr5G.tcw.ws.set_mode(mode = enums.Mode.DRAT) \n
		Switches between the detection rate (Pd) and the false detection rate (Pfa) . \n
			:param mode: DRAT| FDR DRAT Pd is defined as the probability of detection of preamble. FDR Pfa is defined as the total probability of false detection of the preamble.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.Mode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:MODE {param}')

	def get_plevel(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:PLEVel \n
		Snippet: value: float = driver.source.bb.nr5G.tcw.ws.get_plevel() \n
		Specifies the power level of the wanted signal. \n
			:return: ws_pow_lev: float Range: -145 to 20, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:PLEVel?')
		return Conversions.str_to_float(response)

	def set_plevel(self, ws_pow_lev: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:PLEVel \n
		Snippet: driver.source.bb.nr5G.tcw.ws.set_plevel(ws_pow_lev = 1.0) \n
		Specifies the power level of the wanted signal. \n
			:param ws_pow_lev: float Range: -145 to 20, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(ws_pow_lev)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:PLEVel {param}')

	# noinspection PyTypeChecker
	def get_pro_condition(self) -> enums.PropagCond:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:PROCondition \n
		Snippet: value: enums.PropagCond = driver.source.bb.nr5G.tcw.ws.get_pro_condition() \n
		The propagation conditions define the multipath fading environment. They indicated as a combination of channel model name
		and maximum Doppler frequency, i.e. TDLA<DS>-<Doppler> where <DS> indicates the desired delay spread and <Doppler>
		indicates the maximum Doppler frequency. \n
			:return: propag_cond: TDLB100D400| TDLC300D100| TDLA30D10| AWGN| TDLA30D300| TDLA30D75
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:PROCondition?')
		return Conversions.str_to_scalar_enum(response, enums.PropagCond)

	def set_pro_condition(self, propag_cond: enums.PropagCond) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:PROCondition \n
		Snippet: driver.source.bb.nr5G.tcw.ws.set_pro_condition(propag_cond = enums.PropagCond.AWGN) \n
		The propagation conditions define the multipath fading environment. They indicated as a combination of channel model name
		and maximum Doppler frequency, i.e. TDLA<DS>-<Doppler> where <DS> indicates the desired delay spread and <Doppler>
		indicates the maximum Doppler frequency. \n
			:param propag_cond: TDLB100D400| TDLC300D100| TDLA30D10| AWGN| TDLA30D300| TDLA30D75
		"""
		param = Conversions.enum_scalar_to_str(propag_cond, enums.PropagCond)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:PROCondition {param}')

	def get_rb_offset(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:RBOFfset \n
		Snippet: value: int = driver.source.bb.nr5G.tcw.ws.get_rb_offset() \n
		Sets the resource block offset of the wanted signal. \n
			:return: ws_rb_offset: integer Number of resource blocks. Range: 0 to 273
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:RBOFfset?')
		return Conversions.str_to_int(response)

	def set_rb_offset(self, ws_rb_offset: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:RBOFfset \n
		Snippet: driver.source.bb.nr5G.tcw.ws.set_rb_offset(ws_rb_offset = 1) \n
		Sets the resource block offset of the wanted signal. \n
			:param ws_rb_offset: integer Number of resource blocks. Range: 0 to 273
		"""
		param = Conversions.decimal_value_to_str(ws_rb_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:RBOFfset {param}')

	def get_rf_frequency(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:RFFRequency \n
		Snippet: value: int = driver.source.bb.nr5G.tcw.ws.get_rf_frequency() \n
		Sets the RF frequency of the wanted signal. \n
			:return: ws_rf_freq: integer Range: 100e+03 to 6e+09
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:RFFRequency?')
		return Conversions.str_to_int(response)

	def set_rf_frequency(self, ws_rf_freq: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:RFFRequency \n
		Snippet: driver.source.bb.nr5G.tcw.ws.set_rf_frequency(ws_rf_freq = 1) \n
		Sets the RF frequency of the wanted signal. \n
			:param ws_rf_freq: integer Range: 100e+03 to 6e+09
		"""
		param = Conversions.decimal_value_to_str(ws_rf_freq)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:RFFRequency {param}')

	# noinspection PyTypeChecker
	def get_sc_spacing(self) -> enums.Numerology:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:SCSPacing \n
		Snippet: value: enums.Numerology = driver.source.bb.nr5G.tcw.ws.get_sc_spacing() \n
		Sets the subcarrier spacing. \n
			:return: ws_sub_car_spacing: N15| N30| N60| X60| N120| N240 N15, N30, N60, N120, N240 Normal cyclic prefix, value in kHz E60 Extended cyclic prefix, 60 kHz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:SCSPacing?')
		return Conversions.str_to_scalar_enum(response, enums.Numerology)

	def set_sc_spacing(self, ws_sub_car_spacing: enums.Numerology) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:SCSPacing \n
		Snippet: driver.source.bb.nr5G.tcw.ws.set_sc_spacing(ws_sub_car_spacing = enums.Numerology.N120) \n
		Sets the subcarrier spacing. \n
			:param ws_sub_car_spacing: N15| N30| N60| X60| N120| N240 N15, N30, N60, N120, N240 Normal cyclic prefix, value in kHz E60 Extended cyclic prefix, 60 kHz
		"""
		param = Conversions.enum_scalar_to_str(ws_sub_car_spacing, enums.Numerology)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:SCSPacing {param}')

	def get_sym_number(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:SYMNumber \n
		Snippet: value: int = driver.source.bb.nr5G.tcw.ws.get_sym_number() \n
		Sets the number of used OFDM symbols. The starting symbol index is 13 for 1 OFDM symbol and 12 for 2 OFDM symbols. \n
			:return: symbol_number: integer Range: 1 to 14
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:SYMNumber?')
		return Conversions.str_to_int(response)

	def set_sym_number(self, symbol_number: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:SYMNumber \n
		Snippet: driver.source.bb.nr5G.tcw.ws.set_sym_number(symbol_number = 1) \n
		Sets the number of used OFDM symbols. The starting symbol index is 13 for 1 OFDM symbol and 12 for 2 OFDM symbols. \n
			:param symbol_number: integer Range: 1 to 14
		"""
		param = Conversions.decimal_value_to_str(symbol_number)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:SYMNumber {param}')

	def get_tapos(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:TAPos \n
		Snippet: value: int = driver.source.bb.nr5G.tcw.ws.get_tapos() \n
		Sets the position of first DM-RS symbol for PUSCH (and PDSCH) mapping type A (dmrs-TypeA-Position) . \n
			:return: ws_typea_pos: integer Range: 2 to 3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:TAPos?')
		return Conversions.str_to_int(response)

	def set_tapos(self, ws_typea_pos: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:TAPos \n
		Snippet: driver.source.bb.nr5G.tcw.ws.set_tapos(ws_typea_pos = 1) \n
		Sets the position of first DM-RS symbol for PUSCH (and PDSCH) mapping type A (dmrs-TypeA-Position) . \n
			:param ws_typea_pos: integer Range: 2 to 3
		"""
		param = Conversions.decimal_value_to_str(ws_typea_pos)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:TAPos {param}')

	def get_tio_base(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:TIOBase \n
		Snippet: value: float = driver.source.bb.nr5G.tcw.ws.get_tio_base() \n
		Queries the timing off base value. \n
			:return: timing_off_base: float Range: 0 to 6.2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:TIOBase?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_tsetup(self) -> enums.TestSetup:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:TSETup \n
		Snippet: value: enums.TestSetup = driver.source.bb.nr5G.tcw.ws.get_tsetup() \n
		With the test setup selector, the signal definitions can be switched. \n
			:return: test_setup: TS_1| TS_2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:TSETup?')
		return Conversions.str_to_scalar_enum(response, enums.TestSetup)

	def set_tsetup(self, test_setup: enums.TestSetup) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:TSETup \n
		Snippet: driver.source.bb.nr5G.tcw.ws.set_tsetup(test_setup = enums.TestSetup.TS_1) \n
		With the test setup selector, the signal definitions can be switched. \n
			:param test_setup: TS_1| TS_2
		"""
		param = Conversions.enum_scalar_to_str(test_setup, enums.TestSetup)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:TSETup {param}')

	def get_ueid(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:UEID \n
		Snippet: value: int = driver.source.bb.nr5G.tcw.ws.get_ueid() \n
		Sets the UE ID. \n
			:return: ws_ueid: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:UEID?')
		return Conversions.str_to_int(response)

	def set_ueid(self, ws_ueid: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:UEID \n
		Snippet: driver.source.bb.nr5G.tcw.ws.set_ueid(ws_ueid = 1) \n
		Sets the UE ID. \n
			:param ws_ueid: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(ws_ueid)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:UEID {param}')

	def clone(self) -> 'Ws':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ws(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
