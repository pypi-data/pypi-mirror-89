from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Time:
	"""Time commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("time", core, parent)

	@property
	def premp(self):
		"""premp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_premp'):
			from .Time_.Premp import Premp
			self._premp = Premp(self._core, self._base)
		return self._premp

	@property
	def prepre(self):
		"""prepre commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prepre'):
			from .Time_.Prepre import Prepre
			self._prepre = Prepre(self._core, self._base)
		return self._prepre

	def clone(self) -> 'Time':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Time(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
