from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Feed:
	"""Feed commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("feed", core, parent)

	def set(self, feed: enums.MeasRespTimeGate, channel=repcap.Channel.Default) -> None:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:GATE<CH>:FEED \n
		Snippet: driver.calculate.power.sweep.time.gate.feed.set(feed = enums.MeasRespTimeGate.TRAC1, channel = repcap.Channel.Default) \n
		Selects the trace for time gated measurement. Both gates are assigned to the same trace. \n
			:param feed: TRAC1| TRAC2| TRAC3| TRACe1| TRACe2| TRACe3| TRAC4| TRACe4
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gate')"""
		param = Conversions.enum_scalar_to_str(feed, enums.MeasRespTimeGate)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'CALCulate:POWer:SWEep:TIME:GATE{channel_cmd_val}:FEED {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.MeasRespTimeGate:
		"""SCPI: CALCulate:[POWer]:SWEep:TIME:GATE<CH>:FEED \n
		Snippet: value: enums.MeasRespTimeGate = driver.calculate.power.sweep.time.gate.feed.get(channel = repcap.Channel.Default) \n
		Selects the trace for time gated measurement. Both gates are assigned to the same trace. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gate')
			:return: feed: TRAC1| TRAC2| TRAC3| TRACe1| TRACe2| TRACe3| TRAC4| TRACe4"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'CALCulate:POWer:SWEep:TIME:GATE{channel_cmd_val}:FEED?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespTimeGate)
