from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:GATE<CH>:STATe \n
		Snippet: driver.calculate.power.sweep.time.gate.state.set(state = False, channel = repcap.Channel.Default) \n
		Activates the gate settings for the selected trace. The measurement is started with command SENS:POW:INIT. Both gates are
		active at one time. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gate')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'CALCulate:POWer:SWEep:TIME:GATE{channel_cmd_val}:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:GATE<CH>:STATe \n
		Snippet: value: bool = driver.calculate.power.sweep.time.gate.state.get(channel = repcap.Channel.Default) \n
		Activates the gate settings for the selected trace. The measurement is started with command SENS:POW:INIT. Both gates are
		active at one time. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gate')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'CALCulate:POWer:SWEep:TIME:GATE{channel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
