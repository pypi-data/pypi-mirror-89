from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fstate:
	"""Fstate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fstate", core, parent)

	def set(self, fs_tate: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:MARKer<CH>:FSTate \n
		Snippet: driver.source.sweep.frequency.marker.fstate.set(fs_tate = False, channel = repcap.Channel.Default) \n
		Activates the selected marker. \n
			:param fs_tate: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Marker')"""
		param = Conversions.bool_to_str(fs_tate)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:FREQuency:MARKer{channel_cmd_val}:FSTate {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:MARKer<CH>:FSTate \n
		Snippet: value: bool = driver.source.sweep.frequency.marker.fstate.get(channel = repcap.Channel.Default) \n
		Activates the selected marker. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Marker')
			:return: fs_tate: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:SWEep:FREQuency:MARKer{channel_cmd_val}:FSTate?')
		return Conversions.str_to_bool(response)
