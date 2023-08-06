from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scrambler:
	"""Scrambler commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scrambler", core, parent)

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Scrambler_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Scrambler_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	def clone(self) -> 'Scrambler':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Scrambler(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
