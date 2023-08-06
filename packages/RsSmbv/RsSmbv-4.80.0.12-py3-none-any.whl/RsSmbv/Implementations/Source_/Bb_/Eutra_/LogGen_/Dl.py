from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dl:
	"""Dl commands group definition. 9 total commands, 3 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dl", core, parent)

	@property
	def dall(self):
		"""dall commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dall'):
			from .Dl_.Dall import Dall
			self._dall = Dall(self._core, self._base)
		return self._dall

	@property
	def eall(self):
		"""eall commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eall'):
			from .Dl_.Eall import Eall
			self._eall = Eall(self._core, self._base)
		return self._eall

	@property
	def logPoint(self):
		"""logPoint commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_logPoint'):
			from .Dl_.LogPoint import LogPoint
			self._logPoint = LogPoint(self._core, self._base)
		return self._logPoint

	def get_ed_logging(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:LOGGen:DL:EDLogging \n
		Snippet: value: bool = driver.source.bb.eutra.logGen.dl.get_ed_logging() \n
		No command help available \n
			:return: ext_dci_log: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:DL:EDLogging?')
		return Conversions.str_to_bool(response)

	def set_ed_logging(self, ext_dci_log: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:LOGGen:DL:EDLogging \n
		Snippet: driver.source.bb.eutra.logGen.dl.set_ed_logging(ext_dci_log = False) \n
		No command help available \n
			:param ext_dci_log: No help available
		"""
		param = Conversions.bool_to_str(ext_dci_log)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:DL:EDLogging {param}')

	def get_encc(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:LOGGen:DL:ENCC \n
		Snippet: value: bool = driver.source.bb.eutra.logGen.dl.get_encc() \n
		No command help available \n
			:return: encc_log_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:DL:ENCC?')
		return Conversions.str_to_bool(response)

	def set_encc(self, encc_log_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:LOGGen:DL:ENCC \n
		Snippet: driver.source.bb.eutra.logGen.dl.set_encc(encc_log_state = False) \n
		No command help available \n
			:param encc_log_state: No help available
		"""
		param = Conversions.bool_to_str(encc_log_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:DL:ENCC {param}')

	def get_nwus(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:LOGGen:DL:NWUS \n
		Snippet: value: bool = driver.source.bb.eutra.logGen.dl.get_nwus() \n
		No command help available \n
			:return: nwus: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:DL:NWUS?')
		return Conversions.str_to_bool(response)

	def set_nwus(self, nwus: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:LOGGen:DL:NWUS \n
		Snippet: driver.source.bb.eutra.logGen.dl.set_nwus(nwus = False) \n
		No command help available \n
			:param nwus: No help available
		"""
		param = Conversions.bool_to_str(nwus)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:DL:NWUS {param}')

	def get_pbch(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:LOGGen:DL:PBCH \n
		Snippet: value: bool = driver.source.bb.eutra.logGen.dl.get_pbch() \n
		No command help available \n
			:return: pbch_log_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:DL:PBCH?')
		return Conversions.str_to_bool(response)

	def set_pbch(self, pbch_log_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:LOGGen:DL:PBCH \n
		Snippet: driver.source.bb.eutra.logGen.dl.set_pbch(pbch_log_state = False) \n
		No command help available \n
			:param pbch_log_state: No help available
		"""
		param = Conversions.bool_to_str(pbch_log_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:DL:PBCH {param}')

	def get_pdsch(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:LOGGen:DL:PDSCh \n
		Snippet: value: bool = driver.source.bb.eutra.logGen.dl.get_pdsch() \n
		No command help available \n
			:return: pdsch_log_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:DL:PDSCh?')
		return Conversions.str_to_bool(response)

	def set_pdsch(self, pdsch_log_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:LOGGen:DL:PDSCh \n
		Snippet: driver.source.bb.eutra.logGen.dl.set_pdsch(pdsch_log_state = False) \n
		No command help available \n
			:param pdsch_log_state: No help available
		"""
		param = Conversions.bool_to_str(pdsch_log_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:DL:PDSCh {param}')

	def get_pmch(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:LOGGen:DL:PMCH \n
		Snippet: value: bool = driver.source.bb.eutra.logGen.dl.get_pmch() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:DL:PMCH?')
		return Conversions.str_to_bool(response)

	def set_pmch(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:LOGGen:DL:PMCH \n
		Snippet: driver.source.bb.eutra.logGen.dl.set_pmch(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:DL:PMCH {param}')

	def clone(self) -> 'Dl':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dl(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
