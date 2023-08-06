from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Uppts:
	"""Uppts commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("uppts", core, parent)

	@property
	def ldMrs(self):
		"""ldMrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ldMrs'):
			from .Uppts_.LdMrs import LdMrs
			self._ldMrs = LdMrs(self._core, self._base)
		return self._ldMrs

	@property
	def nsym(self):
		"""nsym commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsym'):
			from .Uppts_.Nsym import Nsym
			self._nsym = Nsym(self._core, self._base)
		return self._nsym

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Uppts_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def clone(self) -> 'Uppts':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Uppts(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
