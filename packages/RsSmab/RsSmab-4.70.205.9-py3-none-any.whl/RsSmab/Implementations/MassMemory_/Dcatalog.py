from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dcatalog:
	"""Dcatalog commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dcatalog", core, parent)

	@property
	def length(self):
		"""length commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_length'):
			from .Dcatalog_.Length import Length
			self._length = Length(self._core, self._base)
		return self._length

	def get_value(self) -> str:
		"""SCPI: MMEMory:DCATalog \n
		Snippet: value: str = driver.massMemory.dcatalog.get_value() \n
		Returns the subdirectories of a particular directory. \n
			:return: dcatalog: No help available
		"""
		response = self._core.io.query_str('MMEMory:DCATalog?')
		return trim_str_response(response)

	def clone(self) -> 'Dcatalog':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dcatalog(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
