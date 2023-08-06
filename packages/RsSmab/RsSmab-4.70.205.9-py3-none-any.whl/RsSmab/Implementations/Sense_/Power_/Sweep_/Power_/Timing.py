from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Timing:
	"""Timing commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("timing", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.MeasRespTimingMode:
		"""SCPI: SENSe:[POWer]:SWEep:POWer:TIMing:[MODE] \n
		Snippet: value: enums.MeasRespTimingMode = driver.sense.power.sweep.power.timing.get_mode() \n
		Selects the timing mode of the measurement. \n
			:return: mode: FAST| NORMal| HPRecision | FAST| NORMal FAST Selection FAST leads to a fast measurement with a short integration times for each measurement step. NORMal NORMal leads to a longer but more precise measurement due to a higher integration time for each step.
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:POWer:TIMing:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespTimingMode)

	def set_mode(self, mode: enums.MeasRespTimingMode) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:POWer:TIMing:[MODE] \n
		Snippet: driver.sense.power.sweep.power.timing.set_mode(mode = enums.MeasRespTimingMode.FAST) \n
		Selects the timing mode of the measurement. \n
			:param mode: FAST| NORMal| HPRecision | FAST| NORMal FAST Selection FAST leads to a fast measurement with a short integration times for each measurement step. NORMal NORMal leads to a longer but more precise measurement due to a higher integration time for each step.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.MeasRespTimingMode)
		self._core.io.write(f'SENSe:POWer:SWEep:POWer:TIMing:MODE {param}')
