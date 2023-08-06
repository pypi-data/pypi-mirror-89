from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Range:
	"""Range commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("range", core, parent)

	def get_lower(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:RANGe:LOWer \n
		Snippet: value: float = driver.source.power.range.get_lower() \n
		Queries the current interruption-free range of the level. \n
			:return: lower: float Unit: dBm
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:RANGe:LOWer?')
		return Conversions.str_to_float(response)

	def get_max(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:RANGe:MAX \n
		Snippet: value: float = driver.source.power.range.get_max() \n
		No command help available \n
			:return: pow_range_max: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:RANGe:MAX?')
		return Conversions.str_to_float(response)

	def get_min(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:RANGe:MIN \n
		Snippet: value: float = driver.source.power.range.get_min() \n
		No command help available \n
			:return: pow_range_min: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:RANGe:MIN?')
		return Conversions.str_to_float(response)

	def get_upper(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:RANGe:UPPer \n
		Snippet: value: float = driver.source.power.range.get_upper() \n
		Queries the current interruption-free range of the level. \n
			:return: upper: float Unit: dBm
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:RANGe:UPPer?')
		return Conversions.str_to_float(response)
