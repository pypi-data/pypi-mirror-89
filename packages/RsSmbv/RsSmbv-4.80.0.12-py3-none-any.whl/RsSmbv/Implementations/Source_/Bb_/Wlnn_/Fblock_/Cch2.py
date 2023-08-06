from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cch2:
	"""Cch2 commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cch2", core, parent)

	@property
	def muNum(self):
		"""muNum commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_muNum'):
			from .Cch2_.MuNum import MuNum
			self._muNum = MuNum(self._core, self._base)
		return self._muNum

	@property
	def ruSelection(self):
		"""ruSelection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ruSelection'):
			from .Cch2_.RuSelection import RuSelection
			self._ruSelection = RuSelection(self._core, self._base)
		return self._ruSelection

	def clone(self) -> 'Cch2':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cch2(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
