from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Coordinates:
	"""Coordinates commands group definition. 6 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("coordinates", core, parent)

	@property
	def decimal(self):
		"""decimal commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_decimal'):
			from .Coordinates_.Decimal import Decimal
			self._decimal = Decimal(self._core, self._base)
		return self._decimal

	@property
	def dms(self):
		"""dms commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dms'):
			from .Coordinates_.Dms import Dms
			self._dms = Dms(self._core, self._base)
		return self._dms

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .Coordinates_.FormatPy import FormatPy
			self._formatPy = FormatPy(self._core, self._base)
		return self._formatPy

	@property
	def rframe(self):
		"""rframe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rframe'):
			from .Coordinates_.Rframe import Rframe
			self._rframe = Rframe(self._core, self._base)
		return self._rframe

	def clone(self) -> 'Coordinates':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Coordinates(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
