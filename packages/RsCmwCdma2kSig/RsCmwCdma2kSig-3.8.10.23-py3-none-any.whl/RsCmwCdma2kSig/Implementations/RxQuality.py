from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RxQuality:
	"""RxQuality commands group definition. 27 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rxQuality", core, parent)

	@property
	def tdata(self):
		"""tdata commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tdata'):
			from .RxQuality_.Tdata import Tdata
			self._tdata = Tdata(self._core, self._base)
		return self._tdata

	@property
	def ferfch(self):
		"""ferfch commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_ferfch'):
			from .RxQuality_.Ferfch import Ferfch
			self._ferfch = Ferfch(self._core, self._base)
		return self._ferfch

	@property
	def pstrength(self):
		"""pstrength commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_pstrength'):
			from .RxQuality_.Pstrength import Pstrength
			self._pstrength = Pstrength(self._core, self._base)
		return self._pstrength

	@property
	def fersch(self):
		"""fersch commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_fersch'):
			from .RxQuality_.Fersch import Fersch
			self._fersch = Fersch(self._core, self._base)
		return self._fersch

	@property
	def sfPower(self):
		"""sfPower commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sfPower'):
			from .RxQuality_.SfPower import SfPower
			self._sfPower = SfPower(self._core, self._base)
		return self._sfPower

	def clone(self) -> 'RxQuality':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RxQuality(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
