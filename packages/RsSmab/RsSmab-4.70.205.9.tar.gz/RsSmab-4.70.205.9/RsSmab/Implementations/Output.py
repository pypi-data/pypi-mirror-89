from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from .. import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Output:
	"""Output commands group definition. 12 total commands, 7 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("output", core, parent)

	@property
	def afixed(self):
		"""afixed commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_afixed'):
			from .Output_.Afixed import Afixed
			self._afixed = Afixed(self._core, self._base)
		return self._afixed

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .Output_.All import All
			self._all = All(self._core, self._base)
		return self._all

	@property
	def filterPy(self):
		"""filterPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_filterPy'):
			from .Output_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def fproportional(self):
		"""fproportional commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fproportional'):
			from .Output_.Fproportional import Fproportional
			self._fproportional = Fproportional(self._core, self._base)
		return self._fproportional

	@property
	def protection(self):
		"""protection commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_protection'):
			from .Output_.Protection import Protection
			self._protection = Protection(self._core, self._base)
		return self._protection

	@property
	def user(self):
		"""user commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_user'):
			from .Output_.User import User
			self._user = User(self._core, self._base)
		return self._user

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_state'):
			from .Output_.State import State
			self._state = State(self._core, self._base)
		return self._state

	# noinspection PyTypeChecker
	def get_amode(self) -> enums.PowAttModeOut:
		"""SCPI: OUTPut<HW>:AMODe \n
		Snippet: value: enums.PowAttModeOut = driver.output.get_amode() \n
		Sets the step attenuator mode at the RF output. \n
			:return: am_ode: AUTO| FIXed AUTO The step attenuator adjusts the level settings automatically, within the full variation range. FIXed The step attenuator and amplifier stages are fixed at the current position, providing level settings with constant output VSWR. The resulting variation range is calculated according to the position.
		"""
		response = self._core.io.query_str('OUTPut<HwInstance>:AMODe?')
		return Conversions.str_to_scalar_enum(response, enums.PowAttModeOut)

	def set_amode(self, am_ode: enums.PowAttModeOut) -> None:
		"""SCPI: OUTPut<HW>:AMODe \n
		Snippet: driver.output.set_amode(am_ode = enums.PowAttModeOut.AUTO) \n
		Sets the step attenuator mode at the RF output. \n
			:param am_ode: AUTO| FIXed AUTO The step attenuator adjusts the level settings automatically, within the full variation range. FIXed The step attenuator and amplifier stages are fixed at the current position, providing level settings with constant output VSWR. The resulting variation range is calculated according to the position.
		"""
		param = Conversions.enum_scalar_to_str(am_ode, enums.PowAttModeOut)
		self._core.io.write(f'OUTPut<HwInstance>:AMODe {param}')

	# noinspection PyTypeChecker
	def get_impedance(self) -> enums.InpImpRf:
		"""SCPI: OUTPut<HW>:IMPedance \n
		Snippet: value: enums.InpImpRf = driver.output.get_impedance() \n
		Queries the impedance of the RF outputs. \n
			:return: impedance: G1K| G50| G10K
		"""
		response = self._core.io.query_str('OUTPut<HwInstance>:IMPedance?')
		return Conversions.str_to_scalar_enum(response, enums.InpImpRf)

	def clone(self) -> 'Output':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Output(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
