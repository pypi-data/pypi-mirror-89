from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	@property
	def points(self):
		"""points commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_points'):
			from .Data_.Points import Points
			self._points = Points(self._core, self._base)
		return self._points

	@property
	def xvalues(self):
		"""xvalues commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_xvalues'):
			from .Data_.Xvalues import Xvalues
			self._xvalues = Xvalues(self._core, self._base)
		return self._xvalues

	@property
	def ysValue(self):
		"""ysValue commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ysValue'):
			from .Data_.YsValue import YsValue
			self._ysValue = YsValue(self._core, self._base)
		return self._ysValue

	@property
	def yvalues(self):
		"""yvalues commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_yvalues'):
			from .Data_.Yvalues import Yvalues
			self._yvalues = Yvalues(self._core, self._base)
		return self._yvalues

	def clone(self) -> 'Data':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Data(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
