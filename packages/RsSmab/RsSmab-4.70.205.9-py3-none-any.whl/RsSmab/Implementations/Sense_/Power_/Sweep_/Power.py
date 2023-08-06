from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 18 total commands, 5 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	@property
	def reference(self):
		"""reference commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_reference'):
			from .Power_.Reference import Reference
			self._reference = Reference(self._core, self._base)
		return self._reference

	@property
	def spacing(self):
		"""spacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spacing'):
			from .Power_.Spacing import Spacing
			self._spacing = Spacing(self._core, self._base)
		return self._spacing

	@property
	def timing(self):
		"""timing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_timing'):
			from .Power_.Timing import Timing
			self._timing = Timing(self._core, self._base)
		return self._timing

	@property
	def yscale(self):
		"""yscale commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_yscale'):
			from .Power_.Yscale import Yscale
			self._yscale = Yscale(self._core, self._base)
		return self._yscale

	@property
	def sensor(self):
		"""sensor commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sensor'):
			from .Power_.Sensor import Sensor
			self._sensor = Sensor(self._core, self._base)
		return self._sensor

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.RepeatMode:
		"""SCPI: SENSe:[POWer]:SWEep:POWer:RMODe \n
		Snippet: value: enums.RepeatMode = driver.sense.power.sweep.power.get_rmode() \n
		Selects single or continuous mode for measurement mode power in power analysis. \n
			:return: rm_ode: SINGle| CONTinuous
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:POWer:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.RepeatMode)

	def set_rmode(self, rm_ode: enums.RepeatMode) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:POWer:RMODe \n
		Snippet: driver.sense.power.sweep.power.set_rmode(rm_ode = enums.RepeatMode.CONTinuous) \n
		Selects single or continuous mode for measurement mode power in power analysis. \n
			:param rm_ode: SINGle| CONTinuous
		"""
		param = Conversions.enum_scalar_to_str(rm_ode, enums.RepeatMode)
		self._core.io.write(f'SENSe:POWer:SWEep:POWer:RMODe {param}')

	def get_start(self) -> float:
		"""SCPI: SENSe:[POWer]:SWEep:POWer:STARt \n
		Snippet: value: float = driver.sense.power.sweep.power.get_start() \n
		Sets the start level for the power versus power measurement. \n
			:return: start: float Range: -145 to 20
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:POWer:STARt?')
		return Conversions.str_to_float(response)

	def set_start(self, start: float) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:POWer:STARt \n
		Snippet: driver.sense.power.sweep.power.set_start(start = 1.0) \n
		Sets the start level for the power versus power measurement. \n
			:param start: float Range: -145 to 20
		"""
		param = Conversions.decimal_value_to_str(start)
		self._core.io.write(f'SENSe:POWer:SWEep:POWer:STARt {param}')

	def get_steps(self) -> int:
		"""SCPI: SENSe:[POWer]:SWEep:POWer:STEPs \n
		Snippet: value: int = driver.sense.power.sweep.power.get_steps() \n
		Sets the number of measurement steps for the power versus power measurement. \n
			:return: steps: integer Range: 10 to 1000
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:POWer:STEPs?')
		return Conversions.str_to_int(response)

	def set_steps(self, steps: int) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:POWer:STEPs \n
		Snippet: driver.sense.power.sweep.power.set_steps(steps = 1) \n
		Sets the number of measurement steps for the power versus power measurement. \n
			:param steps: integer Range: 10 to 1000
		"""
		param = Conversions.decimal_value_to_str(steps)
		self._core.io.write(f'SENSe:POWer:SWEep:POWer:STEPs {param}')

	def get_stop(self) -> float:
		"""SCPI: SENSe:[POWer]:SWEep:POWer:STOP \n
		Snippet: value: float = driver.sense.power.sweep.power.get_stop() \n
		Sets the stop level for the power versus power measurement. \n
			:return: stop: float Range: -145 to 20
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:POWer:STOP?')
		return Conversions.str_to_float(response)

	def set_stop(self, stop: float) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:POWer:STOP \n
		Snippet: driver.sense.power.sweep.power.set_stop(stop = 1.0) \n
		Sets the stop level for the power versus power measurement. \n
			:param stop: float Range: -145 to 20
		"""
		param = Conversions.decimal_value_to_str(stop)
		self._core.io.write(f'SENSe:POWer:SWEep:POWer:STOP {param}')

	def clone(self) -> 'Power':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Power(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
