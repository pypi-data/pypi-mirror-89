from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	@property
	def step(self):
		"""step commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_step'):
			from .Power_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step

	def get_value(self) -> float:
		"""SCPI: CSYNthesis:POWer \n
		Snippet: value: float = driver.csynthesis.power.get_value() \n
		Sets the power level of the generated clock signal. \n
			:return: power: float Numerical value Sets the level UP|DOWN Varies the level step by step. The level is increased or decreased by the value set with the command method RsSmab.Csynthesis.Power.value. Range: -24 to 10
		"""
		response = self._core.io.query_str('CSYNthesis:POWer?')
		return Conversions.str_to_float(response)

	def set_value(self, power: float) -> None:
		"""SCPI: CSYNthesis:POWer \n
		Snippet: driver.csynthesis.power.set_value(power = 1.0) \n
		Sets the power level of the generated clock signal. \n
			:param power: float Numerical value Sets the level UP|DOWN Varies the level step by step. The level is increased or decreased by the value set with the command method RsSmab.Csynthesis.Power.value. Range: -24 to 10
		"""
		param = Conversions.decimal_value_to_str(power)
		self._core.io.write(f'CSYNthesis:POWer {param}')

	def clone(self) -> 'Power':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Power(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
