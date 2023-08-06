from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Internal:
	"""Internal commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("internal", core, parent)

	@property
	def deviation(self):
		"""deviation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_deviation'):
			from .Internal_.Deviation import Deviation
			self._deviation = Deviation(self._core, self._base)
		return self._deviation

	# noinspection PyTypeChecker
	def get_source(self) -> enums.AmSourceInt:
		"""SCPI: [SOURce<HW>]:PM:INTernal:SOURce \n
		Snippet: value: enums.AmSourceInt = driver.source.pm.internal.get_source() \n
		No command help available \n
			:return: source: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PM:INTernal:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.AmSourceInt)

	def set_source(self, source: enums.AmSourceInt) -> None:
		"""SCPI: [SOURce<HW>]:PM:INTernal:SOURce \n
		Snippet: driver.source.pm.internal.set_source(source = enums.AmSourceInt.LF1) \n
		No command help available \n
			:param source: No help available
		"""
		param = Conversions.enum_scalar_to_str(source, enums.AmSourceInt)
		self._core.io.write(f'SOURce<HwInstance>:PM:INTernal:SOURce {param}')

	def clone(self) -> 'Internal':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Internal(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
