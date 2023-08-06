from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Parameter:
	"""Parameter commands group definition. 7 total commands, 0 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("parameter", core, parent)

	def get_apco_25(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:FILTer:PARameter:APCO25 \n
		Snippet: value: float = driver.source.bb.w3Gpp.filterPy.parameter.get_apco_25() \n
		The command sets the roll-off factor for filter type APCO25. \n
			:return: apco_25: float Range: 0.05 to 0.99
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:FILTer:PARameter:APCO25?')
		return Conversions.str_to_float(response)

	def set_apco_25(self, apco_25: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:FILTer:PARameter:APCO25 \n
		Snippet: driver.source.bb.w3Gpp.filterPy.parameter.set_apco_25(apco_25 = 1.0) \n
		The command sets the roll-off factor for filter type APCO25. \n
			:param apco_25: float Range: 0.05 to 0.99
		"""
		param = Conversions.decimal_value_to_str(apco_25)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:FILTer:PARameter:APCO25 {param}')

	def get_cosine(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:FILTer:PARameter:COSine \n
		Snippet: value: float = driver.source.bb.w3Gpp.filterPy.parameter.get_cosine() \n
		The command sets the roll-off factor for the Cosine filter type. \n
			:return: cosine: float Range: 0 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:FILTer:PARameter:COSine?')
		return Conversions.str_to_float(response)

	def set_cosine(self, cosine: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:FILTer:PARameter:COSine \n
		Snippet: driver.source.bb.w3Gpp.filterPy.parameter.set_cosine(cosine = 1.0) \n
		The command sets the roll-off factor for the Cosine filter type. \n
			:param cosine: float Range: 0 to 1
		"""
		param = Conversions.decimal_value_to_str(cosine)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:FILTer:PARameter:COSine {param}')

	def get_gauss(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:FILTer:PARameter:GAUSs \n
		Snippet: value: float = driver.source.bb.w3Gpp.filterPy.parameter.get_gauss() \n
		The command sets the roll-off factor for the Gauss filter type. \n
			:return: gauss: float Range: 0.15 to 2.5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:FILTer:PARameter:GAUSs?')
		return Conversions.str_to_float(response)

	def set_gauss(self, gauss: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:FILTer:PARameter:GAUSs \n
		Snippet: driver.source.bb.w3Gpp.filterPy.parameter.set_gauss(gauss = 1.0) \n
		The command sets the roll-off factor for the Gauss filter type. \n
			:param gauss: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(gauss)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:FILTer:PARameter:GAUSs {param}')

	def get_lpass_evm(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:FILTer:PARameter:LPASSEVM \n
		Snippet: value: float = driver.source.bb.w3Gpp.filterPy.parameter.get_lpass_evm() \n
		Sets the cut off frequency factor for the Lowpass (EVM opt.) filter type. \n
			:return: lpass_evm: float Range: 0.05 to 2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:FILTer:PARameter:LPASSEVM?')
		return Conversions.str_to_float(response)

	def set_lpass_evm(self, lpass_evm: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:FILTer:PARameter:LPASSEVM \n
		Snippet: driver.source.bb.w3Gpp.filterPy.parameter.set_lpass_evm(lpass_evm = 1.0) \n
		Sets the cut off frequency factor for the Lowpass (EVM opt.) filter type. \n
			:param lpass_evm: float Range: 0.05 to 2
		"""
		param = Conversions.decimal_value_to_str(lpass_evm)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:FILTer:PARameter:LPASSEVM {param}')

	def get_lpass(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:FILTer:PARameter:LPASs \n
		Snippet: value: float = driver.source.bb.w3Gpp.filterPy.parameter.get_lpass() \n
		Sets the cut off frequency factor for the Lowpass (ACP opt.) filter type. The minimum/maximum values depend on the
		current symbol rate: \n
			:return: lpass: float Range: 0.05 to 2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:FILTer:PARameter:LPASs?')
		return Conversions.str_to_float(response)

	def set_lpass(self, lpass: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:FILTer:PARameter:LPASs \n
		Snippet: driver.source.bb.w3Gpp.filterPy.parameter.set_lpass(lpass = 1.0) \n
		Sets the cut off frequency factor for the Lowpass (ACP opt.) filter type. The minimum/maximum values depend on the
		current symbol rate: \n
			:param lpass: float Range: 0.05 to 2
		"""
		param = Conversions.decimal_value_to_str(lpass)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:FILTer:PARameter:LPASs {param}')

	def get_rcosine(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:FILTer:PARameter:RCOSine \n
		Snippet: value: float = driver.source.bb.w3Gpp.filterPy.parameter.get_rcosine() \n
		The command sets the roll-off factor for the Root Cosine filter type. \n
			:return: rcosine: float Range: 0 to 1.0
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:FILTer:PARameter:RCOSine?')
		return Conversions.str_to_float(response)

	def set_rcosine(self, rcosine: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:FILTer:PARameter:RCOSine \n
		Snippet: driver.source.bb.w3Gpp.filterPy.parameter.set_rcosine(rcosine = 1.0) \n
		The command sets the roll-off factor for the Root Cosine filter type. \n
			:param rcosine: float Range: 0 to 1.0
		"""
		param = Conversions.decimal_value_to_str(rcosine)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:FILTer:PARameter:RCOSine {param}')

	def get_sphase(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:FILTer:PARameter:SPHase \n
		Snippet: value: float = driver.source.bb.w3Gpp.filterPy.parameter.get_sphase() \n
		The command sets B x T for the Split Phase filter type. \n
			:return: sphase: float Range: 0.15 to 2.5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:FILTer:PARameter:SPHase?')
		return Conversions.str_to_float(response)

	def set_sphase(self, sphase: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:FILTer:PARameter:SPHase \n
		Snippet: driver.source.bb.w3Gpp.filterPy.parameter.set_sphase(sphase = 1.0) \n
		The command sets B x T for the Split Phase filter type. \n
			:param sphase: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(sphase)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:FILTer:PARameter:SPHase {param}')
