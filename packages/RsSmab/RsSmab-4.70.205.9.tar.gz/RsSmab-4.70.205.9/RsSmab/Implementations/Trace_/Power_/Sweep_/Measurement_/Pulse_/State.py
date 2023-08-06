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

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:MEASurement:PULSe:STATe \n
		Snippet: value: bool = driver.trace.power.sweep.measurement.pulse.state.get(channel = repcap.Channel.Default) \n
		The above listed commands query the measured pulse parameter values. Note: These commands are only available in time
		measurement mode and with R&S NRP-Z81 power sensors. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: state: float Range: 0 to 100"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'TRACe{channel_cmd_val}:POWer:SWEep:MEASurement:PULSe:STATe?')
		return Conversions.str_to_bool(response)
