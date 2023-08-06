from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Phase:
	"""Phase commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("phase", core, parent)

	@property
	def reference(self):
		"""reference commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reference'):
			from .Phase_.Reference import Reference
			self._reference = Reference(self._core, self._base)
		return self._reference

	def get_value(self) -> float:
		"""SCPI: CSYNthesis:PHASe \n
		Snippet: value: float = driver.csynthesis.phase.get_value() \n
		Shifts the phase of the generated clock signal. \n
			:return: phase: float Range: -36000 to 36000
		"""
		response = self._core.io.query_str('CSYNthesis:PHASe?')
		return Conversions.str_to_float(response)

	def set_value(self, phase: float) -> None:
		"""SCPI: CSYNthesis:PHASe \n
		Snippet: driver.csynthesis.phase.set_value(phase = 1.0) \n
		Shifts the phase of the generated clock signal. \n
			:param phase: float Range: -36000 to 36000
		"""
		param = Conversions.decimal_value_to_str(phase)
		self._core.io.write(f'CSYNthesis:PHASe {param}')

	def clone(self) -> 'Phase':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Phase(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
