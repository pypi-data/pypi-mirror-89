from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:PULSe:STATe \n
		Snippet: driver.sense.power.sweep.time.sensor.pulse.state.set(state = False, channel = repcap.Channel.Default) \n
		Enables pulse data analysis. The measurement is started with command INITiate. Note: The command is only available in
		time measurement mode and with R&S NRP-Z81 power sensors. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:PULSe:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:PULSe:STATe \n
		Snippet: value: bool = driver.sense.power.sweep.time.sensor.pulse.state.get(channel = repcap.Channel.Default) \n
		Enables pulse data analysis. The measurement is started with command INITiate. Note: The command is only available in
		time measurement mode and with R&S NRP-Z81 power sensors. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:PULSe:STATe?')
		return Conversions.str_to_bool(response)
