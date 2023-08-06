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
		"""SCPI: CALCulate:[POWer]:SWEep:FREQuency:MATH<CH>:STATe \n
		Snippet: driver.calculate.power.sweep.frequency.math.state.set(state = False, channel = repcap.Channel.Default) \n
		Activates the trace mathematics mode for 'Frequency' measurement. This feature enables you to calculate the difference
		between the measurement values of two traces. For further calculation, a math result can also be assigned to a trace. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Math')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'CALCulate:POWer:SWEep:FREQuency:MATH{channel_cmd_val}:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: CALCulate:[POWer]:SWEep:FREQuency:MATH<CH>:STATe \n
		Snippet: value: bool = driver.calculate.power.sweep.frequency.math.state.get(channel = repcap.Channel.Default) \n
		Activates the trace mathematics mode for 'Frequency' measurement. This feature enables you to calculate the difference
		between the measurement values of two traces. For further calculation, a math result can also be assigned to a trace. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Math')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'CALCulate:POWer:SWEep:FREQuency:MATH{channel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
