from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Noise:
	"""Noise commands group definition. 5 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("noise", core, parent)

	@property
	def bandwidth(self):
		"""bandwidth commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_bandwidth'):
			from .Noise_.Bandwidth import Bandwidth
			self._bandwidth = Bandwidth(self._core, self._base)
		return self._bandwidth

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_level'):
			from .Noise_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	# noinspection PyTypeChecker
	def get_distribution(self) -> enums.NoisDistrib:
		"""SCPI: [SOURce<HW>]:NOISe:DISTribution \n
		Snippet: value: enums.NoisDistrib = driver.source.noise.get_distribution() \n
		Sets the distribution of the noise power density. \n
			:return: distribution: GAUSs| EQUal
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:NOISe:DISTribution?')
		return Conversions.str_to_scalar_enum(response, enums.NoisDistrib)

	def set_distribution(self, distribution: enums.NoisDistrib) -> None:
		"""SCPI: [SOURce<HW>]:NOISe:DISTribution \n
		Snippet: driver.source.noise.set_distribution(distribution = enums.NoisDistrib.EQUal) \n
		Sets the distribution of the noise power density. \n
			:param distribution: GAUSs| EQUal
		"""
		param = Conversions.enum_scalar_to_str(distribution, enums.NoisDistrib)
		self._core.io.write(f'SOURce<HwInstance>:NOISe:DISTribution {param}')

	def clone(self) -> 'Noise':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Noise(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
