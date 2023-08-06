from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Chirp:
	"""Chirp commands group definition. 9 total commands, 4 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("chirp", core, parent)

	@property
	def compression(self):
		"""compression commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_compression'):
			from .Chirp_.Compression import Compression
			self._compression = Compression(self._core, self._base)
		return self._compression

	@property
	def pulse(self):
		"""pulse commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_pulse'):
			from .Chirp_.Pulse import Pulse
			self._pulse = Pulse(self._core, self._base)
		return self._pulse

	@property
	def test(self):
		"""test commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_test'):
			from .Chirp_.Test import Test
			self._test = Test(self._core, self._base)
		return self._test

	@property
	def trigger(self):
		"""trigger commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_trigger'):
			from .Chirp_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def get_bandwidth(self) -> float:
		"""SCPI: [SOURce<HW>]:CHIRp:BANDwidth \n
		Snippet: value: float = driver.source.chirp.get_bandwidth() \n
		Sets the modulation bandwidth of the chirp modulated signal. \n
			:return: bandwidth: float Range: 0 to Depends on hardware variant
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CHIRp:BANDwidth?')
		return Conversions.str_to_float(response)

	def set_bandwidth(self, bandwidth: float) -> None:
		"""SCPI: [SOURce<HW>]:CHIRp:BANDwidth \n
		Snippet: driver.source.chirp.set_bandwidth(bandwidth = 1.0) \n
		Sets the modulation bandwidth of the chirp modulated signal. \n
			:param bandwidth: float Range: 0 to Depends on hardware variant
		"""
		param = Conversions.decimal_value_to_str(bandwidth)
		self._core.io.write(f'SOURce<HwInstance>:CHIRp:BANDwidth {param}')

	# noinspection PyTypeChecker
	def get_direction(self) -> enums.UpDownDirection:
		"""SCPI: [SOURce<HW>]:CHIRp:DIRection \n
		Snippet: value: enums.UpDownDirection = driver.source.chirp.get_direction() \n
		Selects the direction of the chirp modulation. \n
			:return: direction: DOWN| UP
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CHIRp:DIRection?')
		return Conversions.str_to_scalar_enum(response, enums.UpDownDirection)

	def set_direction(self, direction: enums.UpDownDirection) -> None:
		"""SCPI: [SOURce<HW>]:CHIRp:DIRection \n
		Snippet: driver.source.chirp.set_direction(direction = enums.UpDownDirection.DOWN) \n
		Selects the direction of the chirp modulation. \n
			:param direction: DOWN| UP
		"""
		param = Conversions.enum_scalar_to_str(direction, enums.UpDownDirection)
		self._core.io.write(f'SOURce<HwInstance>:CHIRp:DIRection {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CHIRp:STATe \n
		Snippet: value: bool = driver.source.chirp.get_state() \n
		Activates the generation of a chirp modulation signal. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CHIRp:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CHIRp:STATe \n
		Snippet: driver.source.chirp.set_state(state = False) \n
		Activates the generation of a chirp modulation signal. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:CHIRp:STATe {param}')

	def clone(self) -> 'Chirp':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Chirp(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
