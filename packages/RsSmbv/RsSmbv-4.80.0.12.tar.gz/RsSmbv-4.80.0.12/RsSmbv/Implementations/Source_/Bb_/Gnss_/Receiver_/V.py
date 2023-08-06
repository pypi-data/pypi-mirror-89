from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class V:
	"""V commands group definition. 77 total commands, 7 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("v", core, parent)
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
	def a(self):
		"""a commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_a'):
			from .V_.A import A
			self._a = A(self._core, self._base)
		return self._a

	@property
	def antenna(self):
		"""antenna commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_antenna'):
			from .V_.Antenna import Antenna
			self._antenna = Antenna(self._core, self._base)
		return self._antenna

	@property
	def attitude(self):
		"""attitude commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_attitude'):
			from .V_.Attitude import Attitude
			self._attitude = Attitude(self._core, self._base)
		return self._attitude

	@property
	def environment(self):
		"""environment commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_environment'):
			from .V_.Environment import Environment
			self._environment = Environment(self._core, self._base)
		return self._environment

	@property
	def hil(self):
		"""hil commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_hil'):
			from .V_.Hil import Hil
			self._hil = Hil(self._core, self._base)
		return self._hil

	@property
	def location(self):
		"""location commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_location'):
			from .V_.Location import Location
			self._location = Location(self._core, self._base)
		return self._location

	@property
	def position(self):
		"""position commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_position'):
			from .V_.Position import Position
			self._position = Position(self._core, self._base)
		return self._position

	def clone(self) -> 'V':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = V(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
