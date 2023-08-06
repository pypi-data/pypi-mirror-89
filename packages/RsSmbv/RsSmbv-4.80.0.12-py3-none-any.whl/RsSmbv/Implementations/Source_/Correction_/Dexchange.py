from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dexchange:
	"""Dexchange commands group definition. 8 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dexchange", core, parent)

	@property
	def afile(self):
		"""afile commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_afile'):
			from .Dexchange_.Afile import Afile
			self._afile = Afile(self._core, self._base)
		return self._afile

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Dexchange_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.DexchMode:
		"""SCPI: [SOURce<HW>]:CORRection:DEXChange:MODE \n
		Snippet: value: enums.DexchMode = driver.source.correction.dexchange.get_mode() \n
		Determines import or export of a user correction list. Specify the source or destination file with the command method
		RsSmbv.Source.Correction.Dexchange.select. \n
			:return: mode: IMPort| EXPort
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:DEXChange:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.DexchMode)

	def set_mode(self, mode: enums.DexchMode) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:DEXChange:MODE \n
		Snippet: driver.source.correction.dexchange.set_mode(mode = enums.DexchMode.EXPort) \n
		Determines import or export of a user correction list. Specify the source or destination file with the command method
		RsSmbv.Source.Correction.Dexchange.select. \n
			:param mode: IMPort| EXPort
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.DexchMode)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:DEXChange:MODE {param}')

	def get_select(self) -> str:
		"""SCPI: [SOURce<HW>]:CORRection:DEXChange:SELect \n
		Snippet: value: str = driver.source.correction.dexchange.get_select() \n
		Selects the ASCII file for import or export, containing a user correction list. \n
			:return: filename: string Filename or complete file path; file extension can be omitted.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:DEXChange:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:DEXChange:SELect \n
		Snippet: driver.source.correction.dexchange.set_select(filename = '1') \n
		Selects the ASCII file for import or export, containing a user correction list. \n
			:param filename: string Filename or complete file path; file extension can be omitted.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:DEXChange:SELect {param}')

	def clone(self) -> 'Dexchange':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dexchange(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
