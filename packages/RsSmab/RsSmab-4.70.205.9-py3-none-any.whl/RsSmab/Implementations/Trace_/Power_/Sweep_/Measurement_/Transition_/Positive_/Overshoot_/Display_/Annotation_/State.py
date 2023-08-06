from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:MEASurement:TRANsition:POSitive:OVERshoot:DISPlay:ANNotation:[STATe] \n
		Snippet: driver.trace.power.sweep.measurement.transition.positive.overshoot.display.annotation.state.set(state = False, channel = repcap.Channel.Default) \n
		The above listed commands select the pulse parameters which are indicated in the display and hardcopy file.
		Only six parameters can be indicated at a time. Note: These commands are only available in time measurement mode and with
		R&S NRP-Z81 power sensors. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'TRACe{channel_cmd_val}:POWer:SWEep:MEASurement:TRANsition:POSitive:OVERshoot:DISPlay:ANNotation:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:MEASurement:TRANsition:POSitive:OVERshoot:DISPlay:ANNotation:[STATe] \n
		Snippet: value: bool = driver.trace.power.sweep.measurement.transition.positive.overshoot.display.annotation.state.get(channel = repcap.Channel.Default) \n
		The above listed commands select the pulse parameters which are indicated in the display and hardcopy file.
		Only six parameters can be indicated at a time. Note: These commands are only available in time measurement mode and with
		R&S NRP-Z81 power sensors. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'TRACe{channel_cmd_val}:POWer:SWEep:MEASurement:TRANsition:POSitive:OVERshoot:DISPlay:ANNotation:STATe?')
		return Conversions.str_to_bool(response)
