from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Msas:
	"""Msas commands group definition. 24 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("msas", core, parent)

	@property
	def nmessage(self):
		"""nmessage commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_nmessage'):
			from .Msas_.Nmessage import Nmessage
			self._nmessage = Nmessage(self._core, self._base)
		return self._nmessage

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Msas_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def clone(self) -> 'Msas':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Msas(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
