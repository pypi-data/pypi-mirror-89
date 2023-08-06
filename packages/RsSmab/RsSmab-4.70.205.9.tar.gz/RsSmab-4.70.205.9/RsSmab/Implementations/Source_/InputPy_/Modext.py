from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modext:
	"""Modext commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modext", core, parent)

	@property
	def coupling(self):
		"""coupling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_coupling'):
			from .Modext_.Coupling import Coupling
			self._coupling = Coupling(self._core, self._base)
		return self._coupling

	@property
	def impedance(self):
		"""impedance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_impedance'):
			from .Modext_.Impedance import Impedance
			self._impedance = Impedance(self._core, self._base)
		return self._impedance

	def clone(self) -> 'Modext':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Modext(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
