from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pulse:
	"""Pulse commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pulse", core, parent)

	@property
	def dcycle(self):
		"""dcycle commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dcycle'):
			from .Pulse_.Dcycle import Dcycle
			self._dcycle = Dcycle(self._core, self._base)
		return self._dcycle

	@property
	def period(self):
		"""period commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_period'):
			from .Pulse_.Period import Period
			self._period = Period(self._core, self._base)
		return self._period

	@property
	def width(self):
		"""width commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_width'):
			from .Pulse_.Width import Width
			self._width = Width(self._core, self._base)
		return self._width

	def clone(self) -> 'Pulse':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pulse(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
