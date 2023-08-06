from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Zprs:
	"""Zprs commands group definition. 4 total commands, 4 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("zprs", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def repcap_stream_set(self, enum_value: repcap.Stream) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Stream.Default
		Default value after init: Stream.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_stream_get(self) -> repcap.Stream:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def zp(self):
		"""zp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zp'):
			from .Zprs_.Zp import Zp
			self._zp = Zp(self._core, self._base)
		return self._zp

	@property
	def zpDelta(self):
		"""zpDelta commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zpDelta'):
			from .Zprs_.ZpDelta import ZpDelta
			self._zpDelta = ZpDelta(self._core, self._base)
		return self._zpDelta

	@property
	def zpi(self):
		"""zpi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zpi'):
			from .Zprs_.Zpi import Zpi
			self._zpi = Zpi(self._core, self._base)
		return self._zpi

	@property
	def zpt(self):
		"""zpt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zpt'):
			from .Zprs_.Zpt import Zpt
			self._zpt = Zpt(self._core, self._base)
		return self._zpt

	def clone(self) -> 'Zprs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Zprs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
