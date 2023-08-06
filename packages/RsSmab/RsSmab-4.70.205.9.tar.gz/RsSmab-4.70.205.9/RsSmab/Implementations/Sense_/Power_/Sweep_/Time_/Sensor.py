from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sensor:
	"""Sensor commands group definition. 15 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sensor", core, parent)

	@property
	def offset(self):
		"""offset commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Sensor_.Offset import Offset
			self._offset = Offset(self._core, self._base)
		return self._offset

	@property
	def pulse(self):
		"""pulse commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pulse'):
			from .Sensor_.Pulse import Pulse
			self._pulse = Pulse(self._core, self._base)
		return self._pulse

	@property
	def sfrequency(self):
		"""sfrequency commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfrequency'):
			from .Sensor_.Sfrequency import Sfrequency
			self._sfrequency = Sfrequency(self._core, self._base)
		return self._sfrequency

	@property
	def trigger(self):
		"""trigger commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_trigger'):
			from .Sensor_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def clone(self) -> 'Sensor':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sensor(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
