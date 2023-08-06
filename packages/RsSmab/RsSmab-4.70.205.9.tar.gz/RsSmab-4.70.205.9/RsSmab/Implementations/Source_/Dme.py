from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dme:
	"""Dme commands group definition. 9 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dme", core, parent)

	@property
	def analysis(self):
		"""analysis commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_analysis'):
			from .Dme_.Analysis import Analysis
			self._analysis = Analysis(self._core, self._base)
		return self._analysis

	def get_low_emission(self) -> bool:
		"""SCPI: [SOURce<HW>]:DME:LOWemission \n
		Snippet: value: bool = driver.source.dme.get_low_emission() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:DME:LOWemission?')
		return Conversions.str_to_bool(response)

	def set_low_emission(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:DME:LOWemission \n
		Snippet: driver.source.dme.set_low_emission(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:DME:LOWemission {param}')

	def clone(self) -> 'Dme':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dme(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
