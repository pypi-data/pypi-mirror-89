from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Base:
	"""Base commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("base", core, parent)

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.MeasRespPulsThrBase:
		"""SCPI: TRACe<CH>:[POWer]:SWEep:PULSe:THReshold:BASE \n
		Snippet: value: enums.MeasRespPulsThrBase = driver.trace.power.sweep.pulse.threshold.base.get(channel = repcap.Channel.Default) \n
		Queries how the threshold parameters are calculated. Note: This parameter is only avalaible in time measurement mode and
		R&S NRP-Z81 power sensors. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: base: VOLTage| POWer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'TRACe{channel_cmd_val}:POWer:SWEep:PULSe:THReshold:BASE?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespPulsThrBase)
