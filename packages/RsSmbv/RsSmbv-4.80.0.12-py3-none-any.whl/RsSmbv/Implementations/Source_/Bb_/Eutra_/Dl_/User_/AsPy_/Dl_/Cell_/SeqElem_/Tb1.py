from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tb1:
	"""Tb1 commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tb1", core, parent)

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Tb1_.Mcs import Mcs
			self._mcs = Mcs(self._core, self._base)
		return self._mcs

	@property
	def ndi(self):
		"""ndi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndi'):
			from .Tb1_.Ndi import Ndi
			self._ndi = Ndi(self._core, self._base)
		return self._ndi

	@property
	def rlcCounter(self):
		"""rlcCounter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rlcCounter'):
			from .Tb1_.RlcCounter import RlcCounter
			self._rlcCounter = RlcCounter(self._core, self._base)
		return self._rlcCounter

	@property
	def rv(self):
		"""rv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rv'):
			from .Tb1_.Rv import Rv
			self._rv = Rv(self._core, self._base)
		return self._rv

	def clone(self) -> 'Tb1':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tb1(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
