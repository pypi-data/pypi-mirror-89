from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Time:
	"""Time commands group definition. 8 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("time", core, parent)

	@property
	def gate(self):
		"""gate commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_gate'):
			from .Time_.Gate import Gate
			self._gate = Gate(self._core, self._base)
		return self._gate

	@property
	def math(self):
		"""math commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_math'):
			from .Time_.Math import Math
			self._math = Math(self._core, self._base)
		return self._math

	def clone(self) -> 'Time':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Time(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
