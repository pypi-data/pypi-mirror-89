from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Xvalues:
	"""Xvalues commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("xvalues", core, parent)

	def get(self, channel=repcap.Channel.Default) -> List[float]:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:DATA:XVALues \n
		Snippet: value: List[float] = driver.trace.power.sweep.data.xvalues.get(channel = repcap.Channel.Default) \n
		Queries the x-axis values - frequency, power or time values - of the selected trace of the current power analysis. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: xvalues: string"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_bin_or_ascii_float_list(f'TRACe{channel_cmd_val}:POWer:SWEep:DATA:XVALues?')
		return response
