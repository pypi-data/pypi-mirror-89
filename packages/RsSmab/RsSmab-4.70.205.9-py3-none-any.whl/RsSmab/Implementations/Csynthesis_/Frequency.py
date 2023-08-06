from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	@property
	def step(self):
		"""step commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_step'):
			from .Frequency_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step

	def get_value(self) -> float:
		"""SCPI: CSYNthesis:FREQuency \n
		Snippet: value: float = driver.csynthesis.frequency.get_value() \n
		Sets the frequency of the generated clock signal. \n
			:return: frequency: float Numerical value Sets the frequency UP|DOWN Varies the frequency step by step. The frequency is increased or decreased by the value set with the command method RsSmab.Csynthesis.Frequency.Step.value. Range: 100E3 to 1.5E9
		"""
		response = self._core.io.query_str('CSYNthesis:FREQuency?')
		return Conversions.str_to_float(response)

	def set_value(self, frequency: float) -> None:
		"""SCPI: CSYNthesis:FREQuency \n
		Snippet: driver.csynthesis.frequency.set_value(frequency = 1.0) \n
		Sets the frequency of the generated clock signal. \n
			:param frequency: float Numerical value Sets the frequency UP|DOWN Varies the frequency step by step. The frequency is increased or decreased by the value set with the command method RsSmab.Csynthesis.Frequency.Step.value. Range: 100E3 to 1.5E9
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'CSYNthesis:FREQuency {param}')

	def clone(self) -> 'Frequency':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frequency(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
