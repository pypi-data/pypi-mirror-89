from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class B2I:
	"""B2I commands group definition. 9 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("b2I", core, parent)

	@property
	def data(self):
		"""data commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .B2I_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def power(self):
		"""power commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .B2I_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .B2I_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def clone(self) -> 'B2I':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = B2I(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
