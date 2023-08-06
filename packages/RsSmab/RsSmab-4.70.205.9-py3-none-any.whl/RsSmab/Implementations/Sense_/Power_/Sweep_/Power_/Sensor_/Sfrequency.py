from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sfrequency:
	"""Sfrequency commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sfrequency", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Sfrequency_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def set(self, sfrequency: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:POWer:[SENSor]:SFRequency \n
		Snippet: driver.sense.power.sweep.power.sensor.sfrequency.set(sfrequency = 1.0, channel = repcap.Channel.Default) \n
		Defines the separate frequency used for power vs. power measurement. \n
			:param sfrequency: float Range: 0 to 1E12
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')"""
		param = Conversions.decimal_value_to_str(sfrequency)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:SWEep:POWer:SENSor:SFRequency {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:POWer:[SENSor]:SFRequency \n
		Snippet: value: float = driver.sense.power.sweep.power.sensor.sfrequency.get(channel = repcap.Channel.Default) \n
		Defines the separate frequency used for power vs. power measurement. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: sfrequency: float Range: 0 to 1E12"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:SWEep:POWer:SENSor:SFRequency?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Sfrequency':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sfrequency(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
