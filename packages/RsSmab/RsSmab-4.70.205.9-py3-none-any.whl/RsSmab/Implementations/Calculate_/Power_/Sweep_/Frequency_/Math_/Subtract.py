from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Subtract:
	"""Subtract commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("subtract", core, parent)

	def set(self, subtract: enums.MeasRespMath, channel=repcap.Channel.Default) -> None:
		"""SCPI: CALCulate:[POWer]:SWEep:FREQuency:MATH<CH>:SUBTract \n
		Snippet: driver.calculate.power.sweep.frequency.math.subtract.set(subtract = enums.MeasRespMath.T1REf, channel = repcap.Channel.Default) \n
		Subtracts the operands 1 and 2 and assigns the result to the selected trace in 'Frequency' measurement mode. \n
			:param subtract: T1T1| T1T2| T1T3| T1T4| T1REf| T2T1| T2T2| T2T3| T2T4| T2REf| T3T1| T3T2| T3T3| T3T4| T3REf| T4T1| T4T2| T4T3| T4T4| T4REf
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Math')"""
		param = Conversions.enum_scalar_to_str(subtract, enums.MeasRespMath)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'CALCulate:POWer:SWEep:FREQuency:MATH{channel_cmd_val}:SUBTract {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.MeasRespMath:
		"""SCPI: CALCulate:[POWer]:SWEep:FREQuency:MATH<CH>:SUBTract \n
		Snippet: value: enums.MeasRespMath = driver.calculate.power.sweep.frequency.math.subtract.get(channel = repcap.Channel.Default) \n
		Subtracts the operands 1 and 2 and assigns the result to the selected trace in 'Frequency' measurement mode. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Math')
			:return: subtract: T1T1| T1T2| T1T3| T1T4| T1REf| T2T1| T2T2| T2T3| T2T4| T2REf| T3T1| T3T2| T3T3| T3T4| T3REf| T4T1| T4T2| T4T3| T4T4| T4REf"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'CALCulate:POWer:SWEep:FREQuency:MATH{channel_cmd_val}:SUBTract?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespMath)
