from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Parameter:
	"""Parameter commands group definition. 9 total commands, 1 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("parameter", core, parent)

	@property
	def cosine(self):
		"""cosine commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_cosine'):
			from .Parameter_.Cosine import Cosine
			self._cosine = Cosine(self._core, self._base)
		return self._cosine

	def get_apco_25(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FILTer:PARameter:APCO25 \n
		Snippet: value: float = driver.source.bb.wlnn.filterPy.parameter.get_apco_25() \n
		(for system bandwidth set to 20 MHz only) Sets the roll-off factor for filter type APCO25. \n
			:return: apco_25: float Range: 0.05 to 0.99
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:APCO25?')
		return Conversions.str_to_float(response)

	def set_apco_25(self, apco_25: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FILTer:PARameter:APCO25 \n
		Snippet: driver.source.bb.wlnn.filterPy.parameter.set_apco_25(apco_25 = 1.0) \n
		(for system bandwidth set to 20 MHz only) Sets the roll-off factor for filter type APCO25. \n
			:param apco_25: float Range: 0.05 to 0.99
		"""
		param = Conversions.decimal_value_to_str(apco_25)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:APCO25 {param}')

	def get_gauss(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FILTer:PARameter:GAUSs \n
		Snippet: value: float = driver.source.bb.wlnn.filterPy.parameter.get_gauss() \n
		(for system bandwidth set to 20 MHz only) Sets the roll-off factor for the Gauss filter type. \n
			:return: gauss: float Range: 0.15 to 2.5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:GAUSs?')
		return Conversions.str_to_float(response)

	def set_gauss(self, gauss: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FILTer:PARameter:GAUSs \n
		Snippet: driver.source.bb.wlnn.filterPy.parameter.set_gauss(gauss = 1.0) \n
		(for system bandwidth set to 20 MHz only) Sets the roll-off factor for the Gauss filter type. \n
			:param gauss: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(gauss)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:GAUSs {param}')

	def get_lpass_evm(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FILTer:PARameter:LPASSEVM \n
		Snippet: value: float = driver.source.bb.wlnn.filterPy.parameter.get_lpass_evm() \n
		(for system bandwidth set to 20 MHz only) Sets the cut off frequency factor for the Lowpass (EVM optimization) filter
		type. \n
			:return: lpassevm: float Range: 0.05 to 2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:LPASSEVM?')
		return Conversions.str_to_float(response)

	def set_lpass_evm(self, lpassevm: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FILTer:PARameter:LPASSEVM \n
		Snippet: driver.source.bb.wlnn.filterPy.parameter.set_lpass_evm(lpassevm = 1.0) \n
		(for system bandwidth set to 20 MHz only) Sets the cut off frequency factor for the Lowpass (EVM optimization) filter
		type. \n
			:param lpassevm: float Range: 0.05 to 2
		"""
		param = Conversions.decimal_value_to_str(lpassevm)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:LPASSEVM {param}')

	def get_lpass(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FILTer:PARameter:LPASs \n
		Snippet: value: float = driver.source.bb.wlnn.filterPy.parameter.get_lpass() \n
		(for system bandwidth set to 20 MHz only) Sets the cut off frequency factor for the Lowpass (ACP optimization) filter
		type. \n
			:return: lpass: float Range: 0.05 to 2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:LPASs?')
		return Conversions.str_to_float(response)

	def set_lpass(self, lpass: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FILTer:PARameter:LPASs \n
		Snippet: driver.source.bb.wlnn.filterPy.parameter.set_lpass(lpass = 1.0) \n
		(for system bandwidth set to 20 MHz only) Sets the cut off frequency factor for the Lowpass (ACP optimization) filter
		type. \n
			:param lpass: float Range: 0.05 to 2
		"""
		param = Conversions.decimal_value_to_str(lpass)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:LPASs {param}')

	def get_pgauss(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FILTer:PARameter:PGAuss \n
		Snippet: value: float = driver.source.bb.wlnn.filterPy.parameter.get_pgauss() \n
		(for system bandwidth set to 20 MHz only) Sets the roll-off factor for the pure gauss filter type. \n
			:return: pgauss: float Range: 0.15 to 2.5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:PGAuss?')
		return Conversions.str_to_float(response)

	def set_pgauss(self, pgauss: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FILTer:PARameter:PGAuss \n
		Snippet: driver.source.bb.wlnn.filterPy.parameter.set_pgauss(pgauss = 1.0) \n
		(for system bandwidth set to 20 MHz only) Sets the roll-off factor for the pure gauss filter type. \n
			:param pgauss: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(pgauss)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:PGAuss {param}')

	def get_rcosine(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FILTer:PARameter:RCOSine \n
		Snippet: value: float = driver.source.bb.wlnn.filterPy.parameter.get_rcosine() \n
		(for system bandwidth set to 20 MHz only) Sets the roll-off factor for the root cosine filter type. \n
			:return: rcosine: float Range: 0 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:RCOSine?')
		return Conversions.str_to_float(response)

	def set_rcosine(self, rcosine: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FILTer:PARameter:RCOSine \n
		Snippet: driver.source.bb.wlnn.filterPy.parameter.set_rcosine(rcosine = 1.0) \n
		(for system bandwidth set to 20 MHz only) Sets the roll-off factor for the root cosine filter type. \n
			:param rcosine: float Range: 0 to 1
		"""
		param = Conversions.decimal_value_to_str(rcosine)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:RCOSine {param}')

	def get_sphase(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FILTer:PARameter:SPHase \n
		Snippet: value: float = driver.source.bb.wlnn.filterPy.parameter.get_sphase() \n
		(for system bandwidth set to 20 MHz only) Sets B x T for the Split Phase filter type. \n
			:return: sphase: float Range: 0.15 to 2.5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:SPHase?')
		return Conversions.str_to_float(response)

	def set_sphase(self, sphase: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FILTer:PARameter:SPHase \n
		Snippet: driver.source.bb.wlnn.filterPy.parameter.set_sphase(sphase = 1.0) \n
		(for system bandwidth set to 20 MHz only) Sets B x T for the Split Phase filter type. \n
			:param sphase: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(sphase)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:SPHase {param}')

	def clone(self) -> 'Parameter':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Parameter(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
