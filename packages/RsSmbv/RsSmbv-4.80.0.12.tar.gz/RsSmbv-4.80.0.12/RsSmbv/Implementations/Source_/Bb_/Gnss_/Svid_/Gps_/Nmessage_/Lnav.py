from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lnav:
	"""Lnav commands group definition. 49 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lnav", core, parent)

	@property
	def ccorrection(self):
		"""ccorrection commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccorrection'):
			from .Lnav_.Ccorrection import Ccorrection
			self._ccorrection = Ccorrection(self._core, self._base)
		return self._ccorrection

	@property
	def ephemeris(self):
		"""ephemeris commands group. 27 Sub-classes, 0 commands."""
		if not hasattr(self, '_ephemeris'):
			from .Lnav_.Ephemeris import Ephemeris
			self._ephemeris = Ephemeris(self._core, self._base)
		return self._ephemeris

	def clone(self) -> 'Lnav':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Lnav(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
