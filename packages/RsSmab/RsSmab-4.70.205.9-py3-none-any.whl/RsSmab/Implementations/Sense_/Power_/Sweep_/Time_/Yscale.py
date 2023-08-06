from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Yscale:
	"""Yscale commands group definition. 4 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("yscale", core, parent)

	@property
	def auto(self):
		"""auto commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_auto'):
			from .Yscale_.Auto import Auto
			self._auto = Auto(self._core, self._base)
		return self._auto

	def get_maximum(self) -> float:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:YSCale:MAXimum \n
		Snippet: value: float = driver.sense.power.sweep.time.yscale.get_maximum() \n
		Sets the maximum value for the y axis of the measurement diagram. \n
			:return: maximum: float Range: -200 to 100, Unit: dBm
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:TIME:YSCale:MAXimum?')
		return Conversions.str_to_float(response)

	def set_maximum(self, maximum: float) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:YSCale:MAXimum \n
		Snippet: driver.sense.power.sweep.time.yscale.set_maximum(maximum = 1.0) \n
		Sets the maximum value for the y axis of the measurement diagram. \n
			:param maximum: float Range: -200 to 100, Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(maximum)
		self._core.io.write(f'SENSe:POWer:SWEep:TIME:YSCale:MAXimum {param}')

	def get_minimum(self) -> float:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:YSCale:MINimum \n
		Snippet: value: float = driver.sense.power.sweep.time.yscale.get_minimum() \n
		Sets the minimum value for the y axis of the measurement diagram. \n
			:return: minimum: float Range: -200 to 100
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:TIME:YSCale:MINimum?')
		return Conversions.str_to_float(response)

	def set_minimum(self, minimum: float) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:YSCale:MINimum \n
		Snippet: driver.sense.power.sweep.time.yscale.set_minimum(minimum = 1.0) \n
		Sets the minimum value for the y axis of the measurement diagram. \n
			:param minimum: float Range: -200 to 100
		"""
		param = Conversions.decimal_value_to_str(minimum)
		self._core.io.write(f'SENSe:POWer:SWEep:TIME:YSCale:MINimum {param}')

	def clone(self) -> 'Yscale':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Yscale(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
