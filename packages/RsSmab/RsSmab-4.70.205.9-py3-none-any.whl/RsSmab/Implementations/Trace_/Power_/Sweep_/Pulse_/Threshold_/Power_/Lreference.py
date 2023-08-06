from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lreference:
	"""Lreference commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lreference", core, parent)

	def set(self, lreference: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:PULSe:THReshold:POWer:LREFerence \n
		Snippet: driver.trace.power.sweep.pulse.threshold.power.lreference.set(lreference = 1.0, channel = repcap.Channel.Default) \n
		Queries the lower medial threshold level of the overall pulse level. The proximal power defines the start of the rising
		edge and the end of the falling edge of the pulse. Note: This parameter is only avalaible in time measurement mode and
		R&S NRP-Z81 power sensors. \n
			:param lreference: float Range: 0.0 to 100.0
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')"""
		param = Conversions.decimal_value_to_str(lreference)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'TRACe{channel_cmd_val}:POWer:SWEep:PULSe:THReshold:POWer:LREFerence {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:PULSe:THReshold:POWer:LREFerence \n
		Snippet: value: float = driver.trace.power.sweep.pulse.threshold.power.lreference.get(channel = repcap.Channel.Default) \n
		Queries the lower medial threshold level of the overall pulse level. The proximal power defines the start of the rising
		edge and the end of the falling edge of the pulse. Note: This parameter is only avalaible in time measurement mode and
		R&S NRP-Z81 power sensors. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: lreference: float Range: 0.0 to 100.0"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'TRACe{channel_cmd_val}:POWer:SWEep:PULSe:THReshold:POWer:LREFerence?')
		return Conversions.str_to_float(response)
