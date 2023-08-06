from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Svid:
	"""Svid commands group definition. 2 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("svid", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def azimuth(self):
		"""azimuth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_azimuth'):
			from .Svid_.Azimuth import Azimuth
			self._azimuth = Azimuth(self._core, self._base)
		return self._azimuth

	@property
	def elevation(self):
		"""elevation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_elevation'):
			from .Svid_.Elevation import Elevation
			self._elevation = Elevation(self._core, self._base)
		return self._elevation

	def clone(self) -> 'Svid':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Svid(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
