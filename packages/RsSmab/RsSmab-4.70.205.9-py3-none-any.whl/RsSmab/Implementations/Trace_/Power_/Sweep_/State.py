from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: enums.MeasRespTraceState, channel=repcap.Channel.Default) -> None:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:STATe \n
		Snippet: driver.trace.power.sweep.state.set(state = enums.MeasRespTraceState.HOLD, channel = repcap.Channel.Default) \n
		Activates the selected trace. \n
			:param state: OFF| ON| HOLD
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')"""
		param = Conversions.enum_scalar_to_str(state, enums.MeasRespTraceState)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'TRACe{channel_cmd_val}:POWer:SWEep:STATe {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.MeasRespTraceState:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:STATe \n
		Snippet: value: enums.MeasRespTraceState = driver.trace.power.sweep.state.get(channel = repcap.Channel.Default) \n
		Activates the selected trace. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: state: OFF| ON| HOLD"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'TRACe{channel_cmd_val}:POWer:SWEep:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespTraceState)
