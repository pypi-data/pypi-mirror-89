from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Base:
	"""Base commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("base", core, parent)

	@property
	def display(self):
		"""display commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_display'):
			from .Base_.Display import Display
			self._display = Display(self._core, self._base)
		return self._display

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:MEASurement:POWer:PULSe:BASE \n
		Snippet: value: float = driver.trace.power.sweep.measurement.power.pulse.base.get(channel = repcap.Channel.Default) \n
		The above listed commands query the measured pulse parameter values. Note: These commands are only available in time
		measurement mode and with R&S NRP-Z81 power sensors. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: base: float Range: 0 to 100"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'TRACe{channel_cmd_val}:POWer:SWEep:MEASurement:POWer:PULSe:BASE?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Base':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Base(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
