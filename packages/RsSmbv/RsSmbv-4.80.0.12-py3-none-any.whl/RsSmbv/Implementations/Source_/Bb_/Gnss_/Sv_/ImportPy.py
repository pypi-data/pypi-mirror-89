from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ImportPy:
	"""ImportPy commands group definition. 36 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("importPy", core, parent)

	@property
	def beidou(self):
		"""beidou commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_beidou'):
			from .ImportPy_.Beidou import Beidou
			self._beidou = Beidou(self._core, self._base)
		return self._beidou

	@property
	def galileo(self):
		"""galileo commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_galileo'):
			from .ImportPy_.Galileo import Galileo
			self._galileo = Galileo(self._core, self._base)
		return self._galileo

	@property
	def glonass(self):
		"""glonass commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_glonass'):
			from .ImportPy_.Glonass import Glonass
			self._glonass = Glonass(self._core, self._base)
		return self._glonass

	@property
	def gps(self):
		"""gps commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_gps'):
			from .ImportPy_.Gps import Gps
			self._gps = Gps(self._core, self._base)
		return self._gps

	@property
	def navic(self):
		"""navic commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_navic'):
			from .ImportPy_.Navic import Navic
			self._navic = Navic(self._core, self._base)
		return self._navic

	@property
	def qzss(self):
		"""qzss commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_qzss'):
			from .ImportPy_.Qzss import Qzss
			self._qzss = Qzss(self._core, self._base)
		return self._qzss

	@property
	def sbas(self):
		"""sbas commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sbas'):
			from .ImportPy_.Sbas import Sbas
			self._sbas = Sbas(self._core, self._base)
		return self._sbas

	def clone(self) -> 'ImportPy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ImportPy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
