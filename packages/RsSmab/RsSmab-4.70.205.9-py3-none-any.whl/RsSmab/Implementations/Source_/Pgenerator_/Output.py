from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Output:
	"""Output commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("output", core, parent)

	# noinspection PyTypeChecker
	def get_polarity(self) -> enums.NormInv:
		"""SCPI: [SOURce<HW>]:PGENerator:OUTPut:POLarity \n
		Snippet: value: enums.NormInv = driver.source.pgenerator.output.get_polarity() \n
		Sets the polarity of the pulse output signal. \n
			:return: polarity: NORMal| INVerted NORMal Outputs the pulse signal during the pulse width, that means during the high state. INVerted Inverts the pulse output signal polarity. The pulse output signal is suppressed during the pulse width, but provided during the low state.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PGENerator:OUTPut:POLarity?')
		return Conversions.str_to_scalar_enum(response, enums.NormInv)

	def set_polarity(self, polarity: enums.NormInv) -> None:
		"""SCPI: [SOURce<HW>]:PGENerator:OUTPut:POLarity \n
		Snippet: driver.source.pgenerator.output.set_polarity(polarity = enums.NormInv.INVerted) \n
		Sets the polarity of the pulse output signal. \n
			:param polarity: NORMal| INVerted NORMal Outputs the pulse signal during the pulse width, that means during the high state. INVerted Inverts the pulse output signal polarity. The pulse output signal is suppressed during the pulse width, but provided during the low state.
		"""
		param = Conversions.enum_scalar_to_str(polarity, enums.NormInv)
		self._core.io.write(f'SOURce<HwInstance>:PGENerator:OUTPut:POLarity {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:PGENerator:OUTPut:[STATe] \n
		Snippet: value: bool = driver.source.pgenerator.output.get_state() \n
		Activates the output of the pulse modulation signal. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PGENerator:OUTPut:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:PGENerator:OUTPut:[STATe] \n
		Snippet: driver.source.pgenerator.output.set_state(state = False) \n
		Activates the output of the pulse modulation signal. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:PGENerator:OUTPut:STATe {param}')
