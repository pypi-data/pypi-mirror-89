from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:GATE<CH>:AVERage \n
		Snippet: value: float = driver.calculate.power.sweep.time.gate.average.get(channel = repcap.Channel.Default) \n
		Queries the average power value of the time gated measurement. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gate')
			:return: average: float Range: -1000 to 1000"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'CALCulate:POWer:SWEep:TIME:GATE{channel_cmd_val}:AVERage?')
		return Conversions.str_to_float(response)
