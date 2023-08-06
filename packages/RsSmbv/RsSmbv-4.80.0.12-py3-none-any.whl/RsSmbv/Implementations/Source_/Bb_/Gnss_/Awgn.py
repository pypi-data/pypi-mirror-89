from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Awgn:
	"""Awgn commands group definition. 10 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("awgn", core, parent)

	@property
	def rf(self):
		"""rf commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_rf'):
			from .Awgn_.Rf import Rf
			self._rf = Rf(self._core, self._base)
		return self._rf

	def clone(self) -> 'Awgn':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Awgn(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
