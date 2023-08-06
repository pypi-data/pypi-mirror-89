from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Linear:
	"""Linear commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("linear", core, parent)

	def set(self, depth_lin: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AM<CH>:DEPTh:LINear \n
		Snippet: driver.source.am.depth.linear.set(depth_lin = 1.0, channel = repcap.Channel.Default) \n
		Sets the depth of the linear amplitude modulation in percent / volt. \n
			:param depth_lin: float Range: 0 to 100
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Am')"""
		param = Conversions.decimal_value_to_str(depth_lin)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:AM{channel_cmd_val}:DEPTh:LINear {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:AM<CH>:DEPTh:LINear \n
		Snippet: value: float = driver.source.am.depth.linear.get(channel = repcap.Channel.Default) \n
		Sets the depth of the linear amplitude modulation in percent / volt. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Am')
			:return: depth_lin: float Range: 0 to 100"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AM{channel_cmd_val}:DEPTh:LINear?')
		return Conversions.str_to_float(response)
