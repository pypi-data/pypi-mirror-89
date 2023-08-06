from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Csis:
	"""Csis commands group definition. 17 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("csis", core, parent)

	@property
	def cell(self):
		"""cell commands group. 14 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .Csis_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell

	def clone(self) -> 'Csis':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Csis(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
