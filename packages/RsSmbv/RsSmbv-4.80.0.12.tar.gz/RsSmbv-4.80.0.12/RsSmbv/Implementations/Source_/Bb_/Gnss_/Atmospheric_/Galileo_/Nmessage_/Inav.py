from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Inav:
	"""Inav commands group definition. 3 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("inav", core, parent)

	@property
	def ionospheric(self):
		"""ionospheric commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ionospheric'):
			from .Inav_.Ionospheric import Ionospheric
			self._ionospheric = Ionospheric(self._core, self._base)
		return self._ionospheric

	def clone(self) -> 'Inav':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Inav(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
