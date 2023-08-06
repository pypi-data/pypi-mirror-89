from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trigger", core, parent)

	@property
	def immediate(self):
		"""immediate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_immediate'):
			from .Trigger_.Immediate import Immediate
			self._immediate = Immediate(self._core, self._base)
		return self._immediate

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.PulsTrigModeWithSingle:
		"""SCPI: [SOURce<HW>]:CHIRp:TRIGger:MODE \n
		Snippet: value: enums.PulsTrigModeWithSingle = driver.source.chirp.trigger.get_mode() \n
		Selects the trigger mode for the chirp modulation signal. \n
			:return: mode: AUTO| EXTernal| EGATe| SINGle| ESINgle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CHIRp:TRIGger:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.PulsTrigModeWithSingle)

	def set_mode(self, mode: enums.PulsTrigModeWithSingle) -> None:
		"""SCPI: [SOURce<HW>]:CHIRp:TRIGger:MODE \n
		Snippet: driver.source.chirp.trigger.set_mode(mode = enums.PulsTrigModeWithSingle.AUTO) \n
		Selects the trigger mode for the chirp modulation signal. \n
			:param mode: AUTO| EXTernal| EGATe| SINGle| ESINgle
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.PulsTrigModeWithSingle)
		self._core.io.write(f'SOURce<HwInstance>:CHIRp:TRIGger:MODE {param}')

	def clone(self) -> 'Trigger':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Trigger(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
