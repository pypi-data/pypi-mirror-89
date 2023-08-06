from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sweep:
	"""Sweep commands group definition. 55 total commands, 6 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sweep", core, parent)

	@property
	def color(self):
		"""color commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_color'):
			from .Sweep_.Color import Color
			self._color = Color(self._core, self._base)
		return self._color

	@property
	def data(self):
		"""data commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .Sweep_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def feed(self):
		"""feed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_feed'):
			from .Sweep_.Feed import Feed
			self._feed = Feed(self._core, self._base)
		return self._feed

	@property
	def measurement(self):
		"""measurement commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_measurement'):
			from .Sweep_.Measurement import Measurement
			self._measurement = Measurement(self._core, self._base)
		return self._measurement

	@property
	def pulse(self):
		"""pulse commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pulse'):
			from .Sweep_.Pulse import Pulse
			self._pulse = Pulse(self._core, self._base)
		return self._pulse

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Sweep_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def copy(self, copy: enums.MeasRespTraceCopyDest, channel=repcap.Channel.Default) -> None:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:COPY \n
		Snippet: driver.trace.power.sweep.copy(copy = enums.MeasRespTraceCopyDest.REFerence, channel = repcap.Channel.Default) \n
		Stores the selected trace data as reference trace. \n
			:param copy: REFerence
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')"""
		param = Conversions.enum_scalar_to_str(copy, enums.MeasRespTraceCopyDest)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'TRACe{channel_cmd_val}:POWer:SWEep:COPY {param}')

	def clone(self) -> 'Sweep':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sweep(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
