from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Feed:
	"""Feed commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("feed", core, parent)

	def set(self, feed: enums.MeasRespTraceFeed, channel=repcap.Channel.Default) -> None:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:FEED \n
		Snippet: driver.trace.power.sweep.feed.set(feed = enums.MeasRespTraceFeed.NONE, channel = repcap.Channel.Default) \n
		Selects the source for the trace data. \n
			:param feed: SENS1| SENS2| SENS3| REFerence| NONE| SENSor1| SENSor2| SENSor3| SENS4| SENSor4
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')"""
		param = Conversions.enum_scalar_to_str(feed, enums.MeasRespTraceFeed)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'TRACe{channel_cmd_val}:POWer:SWEep:FEED {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.MeasRespTraceFeed:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:FEED \n
		Snippet: value: enums.MeasRespTraceFeed = driver.trace.power.sweep.feed.get(channel = repcap.Channel.Default) \n
		Selects the source for the trace data. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: feed: SENS1| SENS2| SENS3| REFerence| NONE| SENSor1| SENSor2| SENSor3| SENS4| SENSor4"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'TRACe{channel_cmd_val}:POWer:SWEep:FEED?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespTraceFeed)
