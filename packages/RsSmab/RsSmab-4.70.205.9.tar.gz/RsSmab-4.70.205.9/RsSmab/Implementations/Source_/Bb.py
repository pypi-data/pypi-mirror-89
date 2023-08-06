from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bb:
	"""Bb commands group definition. 17 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bb", core, parent)

	@property
	def dme(self):
		"""dme commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_dme'):
			from .Bb_.Dme import Dme
			self._dme = Dme(self._core, self._base)
		return self._dme

	@property
	def path(self):
		"""path commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_path'):
			from .Bb_.Path import Path
			self._path = Path(self._core, self._base)
		return self._path

	@property
	def vor(self):
		"""vor commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_vor'):
			from .Bb_.Vor import Vor
			self._vor = Vor(self._core, self._base)
		return self._vor

	@property
	def ils(self):
		"""ils commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_ils'):
			from .Bb_.Ils import Ils
			self._ils = Ils(self._core, self._base)
		return self._ils

	def clone(self) -> 'Bb':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bb(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
