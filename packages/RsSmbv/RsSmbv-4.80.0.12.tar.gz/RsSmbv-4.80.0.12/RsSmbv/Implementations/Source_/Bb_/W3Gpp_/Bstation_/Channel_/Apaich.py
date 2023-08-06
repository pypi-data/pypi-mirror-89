from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Apaich:
	"""Apaich commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("apaich", core, parent)

	@property
	def aslot(self):
		"""aslot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aslot'):
			from .Apaich_.Aslot import Aslot
			self._aslot = Aslot(self._core, self._base)
		return self._aslot

	@property
	def saPattern(self):
		"""saPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_saPattern'):
			from .Apaich_.SaPattern import SaPattern
			self._saPattern = SaPattern(self._core, self._base)
		return self._saPattern

	def clone(self) -> 'Apaich':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Apaich(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
