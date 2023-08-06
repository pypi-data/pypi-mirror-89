from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hsupa:
	"""Hsupa commands group definition. 24 total commands, 20 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hsupa", core, parent)

	@property
	def bpayload(self):
		"""bpayload commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bpayload'):
			from .Hsupa_.Bpayload import Bpayload
			self._bpayload = Bpayload(self._core, self._base)
		return self._bpayload

	@property
	def crate(self):
		"""crate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crate'):
			from .Hsupa_.Crate import Crate
			self._crate = Crate(self._core, self._base)
		return self._crate

	@property
	def ctsCount(self):
		"""ctsCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ctsCount'):
			from .Hsupa_.CtsCount import CtsCount
			self._ctsCount = CtsCount(self._core, self._base)
		return self._ctsCount

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Hsupa_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def euctti(self):
		"""euctti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_euctti'):
			from .Hsupa_.Euctti import Euctti
			self._euctti = Euctti(self._core, self._base)
		return self._euctti

	@property
	def frc(self):
		"""frc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frc'):
			from .Hsupa_.Frc import Frc
			self._frc = Frc(self._core, self._base)
		return self._frc

	@property
	def harq(self):
		"""harq commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .Hsupa_.Harq import Harq
			self._harq = Harq(self._core, self._base)
		return self._harq

	@property
	def mibt(self):
		"""mibt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mibt'):
			from .Hsupa_.Mibt import Mibt
			self._mibt = Mibt(self._core, self._base)
		return self._mibt

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Hsupa_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def ncbtti(self):
		"""ncbtti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ncbtti'):
			from .Hsupa_.Ncbtti import Ncbtti
			self._ncbtti = Ncbtti(self._core, self._base)
		return self._ncbtti

	@property
	def rsequence(self):
		"""rsequence commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rsequence'):
			from .Hsupa_.Rsequence import Rsequence
			self._rsequence = Rsequence(self._core, self._base)
		return self._rsequence

	@property
	def rsNumber(self):
		"""rsNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rsNumber'):
			from .Hsupa_.RsNumber import RsNumber
			self._rsNumber = RsNumber(self._core, self._base)
		return self._rsNumber

	@property
	def rvParameter(self):
		"""rvParameter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvParameter'):
			from .Hsupa_.RvParameter import RvParameter
			self._rvParameter = RvParameter(self._core, self._base)
		return self._rvParameter

	@property
	def rvSequence(self):
		"""rvSequence commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvSequence'):
			from .Hsupa_.RvSequence import RvSequence
			self._rvSequence = RvSequence(self._core, self._base)
		return self._rvSequence

	@property
	def sfactor(self):
		"""sfactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfactor'):
			from .Hsupa_.Sfactor import Sfactor
			self._sfactor = Sfactor(self._core, self._base)
		return self._sfactor

	@property
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Hsupa_.Sformat import Sformat
			self._sformat = Sformat(self._core, self._base)
		return self._sformat

	@property
	def tbs(self):
		"""tbs commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tbs'):
			from .Hsupa_.Tbs import Tbs
			self._tbs = Tbs(self._core, self._base)
		return self._tbs

	@property
	def tsCount(self):
		"""tsCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tsCount'):
			from .Hsupa_.TsCount import TsCount
			self._tsCount = TsCount(self._core, self._base)
		return self._tsCount

	@property
	def ttInterval(self):
		"""ttInterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttInterval'):
			from .Hsupa_.TtInterval import TtInterval
			self._ttInterval = TtInterval(self._core, self._base)
		return self._ttInterval

	@property
	def ueCategory(self):
		"""ueCategory commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueCategory'):
			from .Hsupa_.UeCategory import UeCategory
			self._ueCategory = UeCategory(self._core, self._base)
		return self._ueCategory

	def clone(self) -> 'Hsupa':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hsupa(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
