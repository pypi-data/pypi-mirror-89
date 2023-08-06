from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mpath:
	"""Mpath commands group definition. 16 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mpath", core, parent)

	@property
	def v(self):
		"""v commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_v'):
			from .Mpath_.V import V
			self._v = V(self._core, self._base)
		return self._v

	def clone(self) -> 'Mpath':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mpath(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
