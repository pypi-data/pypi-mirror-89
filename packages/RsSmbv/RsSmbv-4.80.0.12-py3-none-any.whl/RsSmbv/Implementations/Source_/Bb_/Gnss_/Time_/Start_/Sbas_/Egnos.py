from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Egnos:
	"""Egnos commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("egnos", core, parent)

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Egnos_.Offset import Offset
			self._offset = Offset(self._core, self._base)
		return self._offset

	@property
	def toWeek(self):
		"""toWeek commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_toWeek'):
			from .Egnos_.ToWeek import ToWeek
			self._toWeek = ToWeek(self._core, self._base)
		return self._toWeek

	@property
	def wnumber(self):
		"""wnumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wnumber'):
			from .Egnos_.Wnumber import Wnumber
			self._wnumber = Wnumber(self._core, self._base)
		return self._wnumber

	def clone(self) -> 'Egnos':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Egnos(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
