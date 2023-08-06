from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def copy(self) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:FREQuency:REFerence:DATA:COPY \n
		Snippet: driver.sense.power.sweep.frequency.reference.data.copy() \n
		Generates a reference curve for 'Frequency' measurement. \n
		"""
		self._core.io.write(f'SENSe:POWer:SWEep:FREQuency:REFerence:DATA:COPY')

	def copy_with_opc(self) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:FREQuency:REFerence:DATA:COPY \n
		Snippet: driver.sense.power.sweep.frequency.reference.data.copy_with_opc() \n
		Generates a reference curve for 'Frequency' measurement. \n
		Same as copy, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SENSe:POWer:SWEep:FREQuency:REFerence:DATA:COPY')

	def get_points(self) -> int:
		"""SCPI: SENSe:[POWer]:SWEep:FREQuency:REFerence:DATA:POINts \n
		Snippet: value: int = driver.sense.power.sweep.frequency.reference.data.get_points() \n
		Queries the number of points from the reference curve in 'Frequency' measurement. \n
			:return: points: integer Range: 10 to 1000
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:FREQuency:REFerence:DATA:POINts?')
		return Conversions.str_to_int(response)

	def get_xvalues(self) -> List[float]:
		"""SCPI: SENSe:[POWer]:SWEep:FREQuency:REFerence:DATA:XVALues \n
		Snippet: value: List[float] = driver.sense.power.sweep.frequency.reference.data.get_xvalues() \n
		Sets or queries the x values of the two reference points, i.e. 'Frequency X (Point A) ' and 'Frequency X (Point B) ' in
		'Frequency' measurement. \n
			:return: xvalues: string
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SENSe:POWer:SWEep:FREQuency:REFerence:DATA:XVALues?')
		return response

	def set_xvalues(self, xvalues: List[float]) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:FREQuency:REFerence:DATA:XVALues \n
		Snippet: driver.sense.power.sweep.frequency.reference.data.set_xvalues(xvalues = [1.1, 2.2, 3.3]) \n
		Sets or queries the x values of the two reference points, i.e. 'Frequency X (Point A) ' and 'Frequency X (Point B) ' in
		'Frequency' measurement. \n
			:param xvalues: string
		"""
		param = Conversions.list_to_csv_str(xvalues)
		self._core.io.write(f'SENSe:POWer:SWEep:FREQuency:REFerence:DATA:XVALues {param}')

	def get_yvalues(self) -> List[float]:
		"""SCPI: SENSe:[POWer]:SWEep:FREQuency:REFerence:DATA:YVALues \n
		Snippet: value: List[float] = driver.sense.power.sweep.frequency.reference.data.get_yvalues() \n
		Sets or queries the y values of the two reference points, i.e.'Pow Y (Point A) ' and 'Power Y (Point B) ' in 'Frequency'
		measurement. \n
			:return: yvalues: string
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SENSe:POWer:SWEep:FREQuency:REFerence:DATA:YVALues?')
		return response

	def set_yvalues(self, yvalues: List[float]) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:FREQuency:REFerence:DATA:YVALues \n
		Snippet: driver.sense.power.sweep.frequency.reference.data.set_yvalues(yvalues = [1.1, 2.2, 3.3]) \n
		Sets or queries the y values of the two reference points, i.e.'Pow Y (Point A) ' and 'Power Y (Point B) ' in 'Frequency'
		measurement. \n
			:param yvalues: string
		"""
		param = Conversions.list_to_csv_str(yvalues)
		self._core.io.write(f'SENSe:POWer:SWEep:FREQuency:REFerence:DATA:YVALues {param}')
