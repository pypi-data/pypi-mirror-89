from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sweep:
	"""Sweep commands group definition. 95 total commands, 4 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sweep", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 5 Sub-classes, 4 commands."""
		if not hasattr(self, '_frequency'):
			from .Sweep_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def hardCopy(self):
		"""hardCopy commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_hardCopy'):
			from .Sweep_.HardCopy import HardCopy
			self._hardCopy = HardCopy(self._core, self._base)
		return self._hardCopy

	@property
	def power(self):
		"""power commands group. 5 Sub-classes, 4 commands."""
		if not hasattr(self, '_power'):
			from .Sweep_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def time(self):
		"""time commands group. 5 Sub-classes, 5 commands."""
		if not hasattr(self, '_time'):
			from .Sweep_.Time import Time
			self._time = Time(self._core, self._base)
		return self._time

	def abort(self, rf_pow_sens_meas_resp_meas_event: bool) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:ABORt \n
		Snippet: driver.sense.power.sweep.abort(rf_pow_sens_meas_resp_meas_event = False) \n
		Aborts the power analysis with NRP power sensors. \n
			:param rf_pow_sens_meas_resp_meas_event: No help available
		"""
		param = Conversions.bool_to_str(rf_pow_sens_meas_resp_meas_event)
		self._core.io.write(f'SENSe:POWer:SWEep:ABORt {param}')

	def initiate(self, rf_pow_sens_meas_resp_meas_event: bool) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:INITiate \n
		Snippet: driver.sense.power.sweep.initiate(rf_pow_sens_meas_resp_meas_event = False) \n
		Starts the power analysis with NRP power sensor. \n
			:param rf_pow_sens_meas_resp_meas_event: No help available
		"""
		param = Conversions.bool_to_str(rf_pow_sens_meas_resp_meas_event)
		self._core.io.write(f'SENSe:POWer:SWEep:INITiate {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.MeasRespMode:
		"""SCPI: SENSe:[POWer]:SWEep:MODE \n
		Snippet: value: enums.MeasRespMode = driver.sense.power.sweep.get_mode() \n
		Selects power versus frequency measurement (frequency response) , power vs power measurement (power sweep, AM/AM) or
		power vs. time measurement. \n
			:return: mode: FREQuency| POWer| TIME
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespMode)

	def set_mode(self, mode: enums.MeasRespMode) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:MODE \n
		Snippet: driver.sense.power.sweep.set_mode(mode = enums.MeasRespMode.FREQuency) \n
		Selects power versus frequency measurement (frequency response) , power vs power measurement (power sweep, AM/AM) or
		power vs. time measurement. \n
			:param mode: FREQuency| POWer| TIME
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.MeasRespMode)
		self._core.io.write(f'SENSe:POWer:SWEep:MODE {param}')

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.RepeatMode:
		"""SCPI: SENSe:[POWer]:SWEep:RMODe \n
		Snippet: value: enums.RepeatMode = driver.sense.power.sweep.get_rmode() \n
		Selects single or continuous mode for power analysis (all measurement modes) . \n
			:return: rm_ode: SINGle| CONTinuous
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.RepeatMode)

	def set_rmode(self, rm_ode: enums.RepeatMode) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:RMODe \n
		Snippet: driver.sense.power.sweep.set_rmode(rm_ode = enums.RepeatMode.CONTinuous) \n
		Selects single or continuous mode for power analysis (all measurement modes) . \n
			:param rm_ode: SINGle| CONTinuous
		"""
		param = Conversions.enum_scalar_to_str(rm_ode, enums.RepeatMode)
		self._core.io.write(f'SENSe:POWer:SWEep:RMODe {param}')

	def clone(self) -> 'Sweep':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sweep(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
