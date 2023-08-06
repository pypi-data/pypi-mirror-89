from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sweep:
	"""Sweep commands group definition. 35 total commands, 4 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sweep", core, parent)

	@property
	def combined(self):
		"""combined commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_combined'):
			from .Sweep_.Combined import Combined
			self._combined = Combined(self._core, self._base)
		return self._combined

	@property
	def marker(self):
		"""marker commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_marker'):
			from .Sweep_.Marker import Marker
			self._marker = Marker(self._core, self._base)
		return self._marker

	@property
	def power(self):
		"""power commands group. 4 Sub-classes, 6 commands."""
		if not hasattr(self, '_power'):
			from .Sweep_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def frequency(self):
		"""frequency commands group. 4 Sub-classes, 7 commands."""
		if not hasattr(self, '_frequency'):
			from .Sweep_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	# noinspection PyTypeChecker
	def get_generation(self) -> enums.FreqSweepType:
		"""SCPI: [SOURce<HW>]:SWEep:GENeration \n
		Snippet: value: enums.FreqSweepType = driver.source.sweep.get_generation() \n
		Selects frequency sweep type. \n
			:return: sweep_type: STEPped| ANALog STEPped Performs a frequency sweep. ANALog Performs a continuous analog frequency sweep (ramp) , synchronized with the sweep time TIME.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:GENeration?')
		return Conversions.str_to_scalar_enum(response, enums.FreqSweepType)

	def set_generation(self, sweep_type: enums.FreqSweepType) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:GENeration \n
		Snippet: driver.source.sweep.set_generation(sweep_type = enums.FreqSweepType.ANALog) \n
		Selects frequency sweep type. \n
			:param sweep_type: STEPped| ANALog STEPped Performs a frequency sweep. ANALog Performs a continuous analog frequency sweep (ramp) , synchronized with the sweep time TIME.
		"""
		param = Conversions.enum_scalar_to_str(sweep_type, enums.FreqSweepType)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:GENeration {param}')

	def reset_all(self) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:RESet:[ALL] \n
		Snippet: driver.source.sweep.reset_all() \n
		Resets all active sweeps to the starting point. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:SWEep:RESet:ALL')

	def reset_all_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:RESet:[ALL] \n
		Snippet: driver.source.sweep.reset_all_with_opc() \n
		Resets all active sweeps to the starting point. \n
		Same as reset_all, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:SWEep:RESet:ALL')

	def clone(self) -> 'Sweep':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sweep(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
