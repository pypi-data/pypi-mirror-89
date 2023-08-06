from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:DISPlay:PERManent:STATe \n
		Snippet: driver.sense.power.display.permanent.state.set(state = False, channel = repcap.Channel.Default) \n
		Activates the permanent display of the measured power level results. The instrument also indicates the sensor type, the
		connection, the measurement source and the offset if set. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:DISPlay:PERManent:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: SENSe<CH>:[POWer]:DISPlay:PERManent:STATe \n
		Snippet: value: bool = driver.sense.power.display.permanent.state.get(channel = repcap.Channel.Default) \n
		Activates the permanent display of the measured power level results. The instrument also indicates the sensor type, the
		connection, the measurement source and the offset if set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:DISPlay:PERManent:STATe?')
		return Conversions.str_to_bool(response)
