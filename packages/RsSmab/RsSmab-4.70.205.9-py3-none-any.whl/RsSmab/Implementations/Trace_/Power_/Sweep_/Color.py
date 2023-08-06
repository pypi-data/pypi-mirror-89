from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Color:
	"""Color commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("color", core, parent)

	def set(self, color: enums.MeasRespTraceColor, channel=repcap.Channel.Default) -> None:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:COLor \n
		Snippet: driver.trace.power.sweep.color.set(color = enums.MeasRespTraceColor.BLUE, channel = repcap.Channel.Default) \n
		Defines the color of a trace. \n
			:param color: INVers| GRAY| YELLow| BLUE| GREen| RED| MAGenta
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')"""
		param = Conversions.enum_scalar_to_str(color, enums.MeasRespTraceColor)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'TRACe{channel_cmd_val}:POWer:SWEep:COLor {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.MeasRespTraceColor:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:COLor \n
		Snippet: value: enums.MeasRespTraceColor = driver.trace.power.sweep.color.get(channel = repcap.Channel.Default) \n
		Defines the color of a trace. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: color: INVers| GRAY| YELLow| BLUE| GREen| RED| MAGenta"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'TRACe{channel_cmd_val}:POWer:SWEep:COLor?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespTraceColor)
