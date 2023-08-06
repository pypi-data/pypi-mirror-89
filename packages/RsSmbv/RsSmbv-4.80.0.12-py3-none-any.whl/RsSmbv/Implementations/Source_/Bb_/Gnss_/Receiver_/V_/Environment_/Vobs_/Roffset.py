from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Roffset:
	"""Roffset commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("roffset", core, parent)

	@property
	def height(self):
		"""height commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_height'):
			from .Roffset_.Height import Height
			self._height = Height(self._core, self._base)
		return self._height

	@property
	def x(self):
		"""x commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_x'):
			from .Roffset_.X import X
			self._x = X(self._core, self._base)
		return self._x

	@property
	def y(self):
		"""y commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_y'):
			from .Roffset_.Y import Y
			self._y = Y(self._core, self._base)
		return self._y

	def clone(self) -> 'Roffset':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Roffset(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
