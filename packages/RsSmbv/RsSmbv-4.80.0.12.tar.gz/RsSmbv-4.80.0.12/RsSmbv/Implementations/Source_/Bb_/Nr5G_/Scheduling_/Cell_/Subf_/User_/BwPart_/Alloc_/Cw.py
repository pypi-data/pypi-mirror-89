from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal.RepeatedCapability import RepeatedCapability
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cw:
	"""Cw commands group definition. 10 total commands, 4 Sub-groups, 0 group commands
	Repeated Capability: Codeword, default value after init: Codeword.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cw", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_codeword_get', 'repcap_codeword_set', repcap.Codeword.Nr0)

	def repcap_codeword_set(self, enum_value: repcap.Codeword) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Codeword.Default
		Default value after init: Codeword.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_codeword_get(self) -> repcap.Codeword:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def mod(self):
		"""mod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mod'):
			from .Cw_.Mod import Mod
			self._mod = Mod(self._core, self._base)
		return self._mod

	@property
	def pdsch(self):
		"""pdsch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdsch'):
			from .Cw_.Pdsch import Pdsch
			self._pdsch = Pdsch(self._core, self._base)
		return self._pdsch

	@property
	def physBits(self):
		"""physBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_physBits'):
			from .Cw_.PhysBits import PhysBits
			self._physBits = PhysBits(self._core, self._base)
		return self._physBits

	@property
	def pusch(self):
		"""pusch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pusch'):
			from .Cw_.Pusch import Pusch
			self._pusch = Pusch(self._core, self._base)
		return self._pusch

	def clone(self) -> 'Cw':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cw(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
