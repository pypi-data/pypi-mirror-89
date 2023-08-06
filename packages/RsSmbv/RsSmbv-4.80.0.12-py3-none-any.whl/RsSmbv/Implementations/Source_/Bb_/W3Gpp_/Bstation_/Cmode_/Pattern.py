from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pattern:
	"""Pattern commands group definition. 4 total commands, 4 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pattern", core, parent)
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
	def tgd(self):
		"""tgd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tgd'):
			from .Pattern_.Tgd import Tgd
			self._tgd = Tgd(self._core, self._base)
		return self._tgd

	@property
	def tgl(self):
		"""tgl commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tgl'):
			from .Pattern_.Tgl import Tgl
			self._tgl = Tgl(self._core, self._base)
		return self._tgl

	@property
	def tgpl(self):
		"""tgpl commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tgpl'):
			from .Pattern_.Tgpl import Tgpl
			self._tgpl = Tgpl(self._core, self._base)
		return self._tgpl

	@property
	def tgsn(self):
		"""tgsn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tgsn'):
			from .Pattern_.Tgsn import Tgsn
			self._tgsn = Tgsn(self._core, self._base)
		return self._tgsn

	def clone(self) -> 'Pattern':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pattern(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
