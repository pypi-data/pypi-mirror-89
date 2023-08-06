from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nprach:
	"""Nprach commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nprach", core, parent)

	@property
	def scind(self):
		"""scind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scind'):
			from .Nprach_.Scind import Scind
			self._scind = Scind(self._core, self._base)
		return self._scind

	@property
	def snumber(self):
		"""snumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_snumber'):
			from .Nprach_.Snumber import Snumber
			self._snumber = Snumber(self._core, self._base)
		return self._snumber

	def clone(self) -> 'Nprach':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nprach(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
