from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vor:
	"""Vor commands group definition. 5 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("vor", core, parent)

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_setting'):
			from .Vor_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:VOR:PRESet \n
		Snippet: driver.source.bb.vor.preset() \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:PRESet')

	def preset_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:VOR:PRESet \n
		Snippet: driver.source.bb.vor.preset_with_opc() \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:VOR:PRESet')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:VOR:STATe \n
		Snippet: value: bool = driver.source.bb.vor.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:VOR:STATe \n
		Snippet: driver.source.bb.vor.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:STATe {param}')

	def clone(self) -> 'Vor':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Vor(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
