from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Position:
	"""Position commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("position", core, parent)

	@property
	def ecef(self):
		"""ecef commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ecef'):
			from .Position_.Ecef import Ecef
			self._ecef = Ecef(self._core, self._base)
		return self._ecef

	@property
	def enu(self):
		"""enu commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enu'):
			from .Position_.Enu import Enu
			self._enu = Enu(self._core, self._base)
		return self._enu

	@property
	def lla(self):
		"""lla commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lla'):
			from .Position_.Lla import Lla
			self._lla = Lla(self._core, self._base)
		return self._lla

	def clone(self) -> 'Position':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Position(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
