from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def set(self, frequency: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:MARKer<CH>:FREQuency \n
		Snippet: driver.source.sweep.frequency.marker.frequency.set(frequency = 1.0, channel = repcap.Channel.Default) \n
		Sets the frequency of the selected marker. \n
			:param frequency: float
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Marker')"""
		param = Conversions.decimal_value_to_str(frequency)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:FREQuency:MARKer{channel_cmd_val}:FREQuency {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:MARKer<CH>:FREQuency \n
		Snippet: value: float = driver.source.sweep.frequency.marker.frequency.get(channel = repcap.Channel.Default) \n
		Sets the frequency of the selected marker. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Marker')
			:return: frequency: float"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:SWEep:FREQuency:MARKer{channel_cmd_val}:FREQuency?')
		return Conversions.str_to_float(response)
