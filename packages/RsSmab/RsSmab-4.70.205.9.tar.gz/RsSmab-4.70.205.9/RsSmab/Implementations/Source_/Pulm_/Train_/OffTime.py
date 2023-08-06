from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OffTime:
	"""OffTime commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("offTime", core, parent)

	def get_points(self) -> int:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:OFFTime:POINts \n
		Snippet: value: int = driver.source.pulm.train.offTime.get_points() \n
		Queries the number of on and off time entries and repetitions in the selected list. \n
			:return: points: integer Range: 0 to INT_MAX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:TRAin:OFFTime:POINts?')
		return Conversions.str_to_int(response)

	def get_value(self) -> List[float]:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:OFFTime \n
		Snippet: value: List[float] = driver.source.pulm.train.offTime.get_value() \n
		Enters the pulse on/off times values in the selected list. \n
			:return: off_time: Offtime#1{, Offtime#2, ...} | binary block data List of comma-separated numeric values or binary block data, where: The list of numbers can be of any length. In binary block format, 8 (4) bytes are always interpreted as a floating-point number with double accuracy. See :​FORMat[:​DATA] for details. The maximum length is 2047 values. Range: 0 ns to 5 ms
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce<HwInstance>:PULM:TRAin:OFFTime?')
		return response

	def set_value(self, off_time: List[float]) -> None:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:OFFTime \n
		Snippet: driver.source.pulm.train.offTime.set_value(off_time = [1.1, 2.2, 3.3]) \n
		Enters the pulse on/off times values in the selected list. \n
			:param off_time: Offtime#1{, Offtime#2, ...} | binary block data List of comma-separated numeric values or binary block data, where: The list of numbers can be of any length. In binary block format, 8 (4) bytes are always interpreted as a floating-point number with double accuracy. See :​FORMat[:​DATA] for details. The maximum length is 2047 values. Range: 0 ns to 5 ms
		"""
		param = Conversions.list_to_csv_str(off_time)
		self._core.io.write(f'SOURce<HwInstance>:PULM:TRAin:OFFTime {param}')
