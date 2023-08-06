from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Is2:
	"""Is2 commands group definition. 7 total commands, 0 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("is2", core, parent)

	# noinspection PyTypeChecker
	def get_chbw(self) -> enums.EutraCaChannelBandwidth:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:IS2:CHBW \n
		Snippet: value: enums.EutraCaChannelBandwidth = driver.source.bb.eutra.tcw.is2.get_chbw() \n
		Queries the channel bandwidth of the interfering signal. \n
			:return: channel_bandwidt: BW20_00| BW10_00| BW5_00| BW3_00| BW1_40| BW15_00
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS2:CHBW?')
		return Conversions.str_to_scalar_enum(response, enums.EutraCaChannelBandwidth)

	# noinspection PyTypeChecker
	def get_duplex(self) -> enums.EutraDuplexMode:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:IS2:DUPLex \n
		Snippet: value: enums.EutraDuplexMode = driver.source.bb.eutra.tcw.is2.get_duplex() \n
		Selects whether TDD or FDD duplexing mode is used. \n
			:return: duplexing: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS2:DUPLex?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDuplexMode)

	def set_duplex(self, duplexing: enums.EutraDuplexMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:IS2:DUPLex \n
		Snippet: driver.source.bb.eutra.tcw.is2.set_duplex(duplexing = enums.EutraDuplexMode.FDD) \n
		Selects whether TDD or FDD duplexing mode is used. \n
			:param duplexing: TDD| FDD
		"""
		param = Conversions.enum_scalar_to_str(duplexing, enums.EutraDuplexMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:IS2:DUPLex {param}')

	# noinspection PyTypeChecker
	def get_if_type(self) -> enums.EutraTcwInterfType:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:IS2:IFTYpe \n
		Snippet: value: enums.EutraTcwInterfType = driver.source.bb.eutra.tcw.is2.get_if_type() \n
			INTRO_CMD_HELP: Selects the type of the interfering signal: \n
			- For Blocking tests, the interfering signal can be an in-band EUTRA/LTE signal (EUTra) or out-of-band CW signal (CW) .
			- For Receiver Intermodulation tests, the first interfering signal can be an EUTRA/LTE signal (EUTra) or narrowband EUTRA signal (NEUTra) . The second interfering signal is always a CW signal (CW) . \n
			:return: interferer_type: NEUTra| EUTra| CW| UTRA
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS2:IFTYpe?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwInterfType)

	def get_ort_cover(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:IS2:ORTCover \n
		Snippet: value: int = driver.source.bb.eutra.tcw.is2.get_ort_cover() \n
		No command help available \n
			:return: ortho_cover: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS2:ORTCover?')
		return Conversions.str_to_int(response)

	def get_plevel(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:IS2:PLEVel \n
		Snippet: value: str = driver.source.bb.eutra.tcw.is2.get_plevel() \n
		Queries the power level of the interfering signal. \n
			:return: power_level: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS2:PLEVel?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_pr_condition(self) -> enums.EutraTcwPropagCond:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:IS2:PRCOndition \n
		Snippet: value: enums.EutraTcwPropagCond = driver.source.bb.eutra.tcw.is2.get_pr_condition() \n
		No command help available \n
			:return: propag_condition: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS2:PRCOndition?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwPropagCond)

	def get_rf_frequency(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:IS2:RFFRequency \n
		Snippet: value: int = driver.source.bb.eutra.tcw.is2.get_rf_frequency() \n
		Queries the center frequency of the interfering signal. \n
			:return: rf_frequency: integer Range: 100E3 to 6E9
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS2:RFFRequency?')
		return Conversions.str_to_int(response)

	def set_rf_frequency(self, rf_frequency: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:IS2:RFFRequency \n
		Snippet: driver.source.bb.eutra.tcw.is2.set_rf_frequency(rf_frequency = 1) \n
		Queries the center frequency of the interfering signal. \n
			:param rf_frequency: integer Range: 100E3 to 6E9
		"""
		param = Conversions.decimal_value_to_str(rf_frequency)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:IS2:RFFRequency {param}')
