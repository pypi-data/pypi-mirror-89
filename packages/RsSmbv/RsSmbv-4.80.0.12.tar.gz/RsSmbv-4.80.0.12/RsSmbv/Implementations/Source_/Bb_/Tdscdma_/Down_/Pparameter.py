from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pparameter:
	"""Pparameter commands group definition. 5 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pparameter", core, parent)

	@property
	def dpch(self):
		"""dpch commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_dpch'):
			from .Pparameter_.Dpch import Dpch
			self._dpch = Dpch(self._core, self._base)
		return self._dpch

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Pparameter_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	@property
	def pccpch(self):
		"""pccpch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pccpch'):
			from .Pparameter_.Pccpch import Pccpch
			self._pccpch = Pccpch(self._core, self._base)
		return self._pccpch

	def clone(self) -> 'Pparameter':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pparameter(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
