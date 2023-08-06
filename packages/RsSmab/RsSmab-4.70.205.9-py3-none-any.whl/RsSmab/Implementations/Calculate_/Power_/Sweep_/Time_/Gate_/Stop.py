from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Stop:
	"""Stop commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stop", core, parent)

	def set(self, stop: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:GATE<CH>:STOP \n
		Snippet: driver.calculate.power.sweep.time.gate.stop.set(stop = 1.0, channel = repcap.Channel.Default) \n
		Sets the start time of the selected gate. Insert value and unit. \n
			:param stop: float
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gate')"""
		param = Conversions.decimal_value_to_str(stop)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'CALCulate:POWer:SWEep:TIME:GATE{channel_cmd_val}:STOP {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:GATE<CH>:STOP \n
		Snippet: value: float = driver.calculate.power.sweep.time.gate.stop.get(channel = repcap.Channel.Default) \n
		Sets the start time of the selected gate. Insert value and unit. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gate')
			:return: stop: float"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'CALCulate:POWer:SWEep:TIME:GATE{channel_cmd_val}:STOP?')
		return Conversions.str_to_float(response)
