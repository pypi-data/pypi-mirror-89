from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from .. import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Csynthesis:
	"""Csynthesis commands group definition. 13 total commands, 4 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("csynthesis", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .Csynthesis_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_offset'):
			from .Csynthesis_.Offset import Offset
			self._offset = Offset(self._core, self._base)
		return self._offset

	@property
	def phase(self):
		"""phase commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_phase'):
			from .Csynthesis_.Phase import Phase
			self._phase = Phase(self._core, self._base)
		return self._phase

	@property
	def power(self):
		"""power commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Csynthesis_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	# noinspection PyTypeChecker
	def get_otype(self) -> enums.ClkSynOutType:
		"""SCPI: CSYNthesis:OTYPe \n
		Snippet: value: enums.ClkSynOutType = driver.csynthesis.get_otype() \n
		Defines the shape of the generated clock signal. \n
			:return: mode: SESine| DSQuare| CMOS| DSINe SESine = single-ended sine DSINe = differential sine DSQuare = differential square CMOS = CMOS
		"""
		response = self._core.io.query_str('CSYNthesis:OTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.ClkSynOutType)

	def set_otype(self, mode: enums.ClkSynOutType) -> None:
		"""SCPI: CSYNthesis:OTYPe \n
		Snippet: driver.csynthesis.set_otype(mode = enums.ClkSynOutType.CMOS) \n
		Defines the shape of the generated clock signal. \n
			:param mode: SESine| DSQuare| CMOS| DSINe SESine = single-ended sine DSINe = differential sine DSQuare = differential square CMOS = CMOS
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ClkSynOutType)
		self._core.io.write(f'CSYNthesis:OTYPe {param}')

	def get_state(self) -> bool:
		"""SCPI: CSYNthesis:STATe \n
		Snippet: value: bool = driver.csynthesis.get_state() \n
		Activates the clock synthesis. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('CSYNthesis:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: CSYNthesis:STATe \n
		Snippet: driver.csynthesis.set_state(state = False) \n
		Activates the clock synthesis. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CSYNthesis:STATe {param}')

	def get_voltage(self) -> float:
		"""SCPI: CSYNthesis:VOLTage \n
		Snippet: value: float = driver.csynthesis.get_voltage() \n
		Sets the voltage for the CMOS signal. \n
			:return: voltage: float Range: 0.8 to 2.7
		"""
		response = self._core.io.query_str('CSYNthesis:VOLTage?')
		return Conversions.str_to_float(response)

	def set_voltage(self, voltage: float) -> None:
		"""SCPI: CSYNthesis:VOLTage \n
		Snippet: driver.csynthesis.set_voltage(voltage = 1.0) \n
		Sets the voltage for the CMOS signal. \n
			:param voltage: float Range: 0.8 to 2.7
		"""
		param = Conversions.decimal_value_to_str(voltage)
		self._core.io.write(f'CSYNthesis:VOLTage {param}')

	def clone(self) -> 'Csynthesis':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Csynthesis(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
