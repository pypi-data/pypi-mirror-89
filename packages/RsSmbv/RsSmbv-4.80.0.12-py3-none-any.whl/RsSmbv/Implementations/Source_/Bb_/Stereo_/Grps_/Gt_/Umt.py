from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Umt:
	"""Umt commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("umt", core, parent)

	@property
	def data(self):
		"""data commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .Umt_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def noEntries(self):
		"""noEntries commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noEntries'):
			from .Umt_.NoEntries import NoEntries
			self._noEntries = NoEntries(self._core, self._base)
		return self._noEntries

	def clone(self) -> 'Umt':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Umt(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
