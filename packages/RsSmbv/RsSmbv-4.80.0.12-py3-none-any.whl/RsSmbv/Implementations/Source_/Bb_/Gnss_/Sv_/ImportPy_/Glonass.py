from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Glonass:
	"""Glonass commands group definition. 4 total commands, 3 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("glonass", core, parent)
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
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Glonass_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	@property
	def file(self):
		"""file commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_file'):
			from .Glonass_.File import File
			self._file = File(self._core, self._base)
		return self._file

	@property
	def udSource(self):
		"""udSource commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_udSource'):
			from .Glonass_.UdSource import UdSource
			self._udSource = UdSource(self._core, self._base)
		return self._udSource

	def clone(self) -> 'Glonass':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Glonass(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
