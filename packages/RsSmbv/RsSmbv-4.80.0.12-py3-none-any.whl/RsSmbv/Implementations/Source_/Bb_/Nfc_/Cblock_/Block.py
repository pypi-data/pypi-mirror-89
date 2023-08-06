from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Block:
	"""Block commands group definition. 5 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("block", core, parent)
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
	def bdata(self):
		"""bdata commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bdata'):
			from .Block_.Bdata import Bdata
			self._bdata = Bdata(self._core, self._base)
		return self._bdata

	@property
	def bnumber(self):
		"""bnumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bnumber'):
			from .Block_.Bnumber import Bnumber
			self._bnumber = Bnumber(self._core, self._base)
		return self._bnumber

	@property
	def len(self):
		"""len commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_len'):
			from .Block_.Len import Len
			self._len = Len(self._core, self._base)
		return self._len

	@property
	def locked(self):
		"""locked commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_locked'):
			from .Block_.Locked import Locked
			self._locked = Locked(self._core, self._base)
		return self._locked

	@property
	def slOrder(self):
		"""slOrder commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slOrder'):
			from .Block_.SlOrder import SlOrder
			self._slOrder = SlOrder(self._core, self._base)
		return self._slOrder

	def clone(self) -> 'Block':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Block(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
