from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tdata:
	"""Tdata commands group definition. 9 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tdata", core, parent)

	@property
	def ferfch(self):
		"""ferfch commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_ferfch'):
			from .Tdata_.Ferfch import Ferfch
			self._ferfch = Ferfch(self._core, self._base)
		return self._ferfch

	@property
	def fersch(self):
		"""fersch commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_fersch'):
			from .Tdata_.Fersch import Fersch
			self._fersch = Fersch(self._core, self._base)
		return self._fersch

	def clone(self) -> 'Tdata':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tdata(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
