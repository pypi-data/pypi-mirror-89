from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Points:
	"""Points commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("points", core, parent)

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:DATA:POINts \n
		Snippet: value: int = driver.trace.power.sweep.data.points.get(channel = repcap.Channel.Default) \n
		Queries the number of measurement points of the selected trace of the current power analysis. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: points: integer Range: 10 to 1000"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'TRACe{channel_cmd_val}:POWer:SWEep:DATA:POINts?')
		return Conversions.str_to_int(response)
