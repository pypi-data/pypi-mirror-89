from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Emtc:
	"""Emtc commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("emtc", core, parent)

	@property
	def arb(self):
		"""arb commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_arb'):
			from .Emtc_.Arb import Arb
			self._arb = Arb(self._core, self._base)
		return self._arb

	@property
	def prAttempts(self):
		"""prAttempts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prAttempts'):
			from .Emtc_.PrAttempts import PrAttempts
			self._prAttempts = PrAttempts(self._core, self._base)
		return self._prAttempts

	def clone(self) -> 'Emtc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Emtc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
