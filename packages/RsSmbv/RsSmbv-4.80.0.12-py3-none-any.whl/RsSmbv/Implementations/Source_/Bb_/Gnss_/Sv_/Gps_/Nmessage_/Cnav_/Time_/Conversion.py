from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Conversion:
	"""Conversion commands group definition. 27 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("conversion", core, parent)

	@property
	def galileo(self):
		"""galileo commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_galileo'):
			from .Conversion_.Galileo import Galileo
			self._galileo = Galileo(self._core, self._base)
		return self._galileo

	@property
	def glonass(self):
		"""glonass commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_glonass'):
			from .Conversion_.Glonass import Glonass
			self._glonass = Glonass(self._core, self._base)
		return self._glonass

	@property
	def utc(self):
		"""utc commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_utc'):
			from .Conversion_.Utc import Utc
			self._utc = Utc(self._core, self._base)
		return self._utc

	def clone(self) -> 'Conversion':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Conversion(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
