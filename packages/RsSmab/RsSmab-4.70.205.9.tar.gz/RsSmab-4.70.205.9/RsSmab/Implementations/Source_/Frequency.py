from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 50 total commands, 6 Sub-groups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	@property
	def multiplier(self):
		"""multiplier commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_multiplier'):
			from .Frequency_.Multiplier import Multiplier
			self._multiplier = Multiplier(self._core, self._base)
		return self._multiplier

	@property
	def phase(self):
		"""phase commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_phase'):
			from .Frequency_.Phase import Phase
			self._phase = Phase(self._core, self._base)
		return self._phase

	@property
	def pll(self):
		"""pll commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pll'):
			from .Frequency_.Pll import Pll
			self._pll = Pll(self._core, self._base)
		return self._pll

	@property
	def step(self):
		"""step commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_step'):
			from .Frequency_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step

	@property
	def cw(self):
		"""cw commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_cw'):
			from .Frequency_.Cw import Cw
			self._cw = Cw(self._core, self._base)
		return self._cw

	@property
	def fixed(self):
		"""fixed commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_fixed'):
			from .Frequency_.Fixed import Fixed
			self._fixed = Fixed(self._core, self._base)
		return self._fixed

	def get_center(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:CENTer \n
		Snippet: value: float = driver.source.frequency.get_center() \n
		Sets the center frequency of the sweep. See 'Correlating Parameters in Sweep Mode'. \n
			:return: center: float Range: 300 kHz to RFmax, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:CENTer?')
		return Conversions.str_to_float(response)

	def set_center(self, center: float) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:CENTer \n
		Snippet: driver.source.frequency.set_center(center = 1.0) \n
		Sets the center frequency of the sweep. See 'Correlating Parameters in Sweep Mode'. \n
			:param center: float Range: 300 kHz to RFmax, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(center)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:CENTer {param}')

	def get_frequency(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:FREQuency \n
		Snippet: value: float = driver.source.frequency.get_frequency() \n
		No command help available \n
			:return: frequency: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:FREQuency \n
		Snippet: driver.source.frequency.set_frequency(frequency = 1.0) \n
		No command help available \n
			:param frequency: No help available
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:FREQuency {param}')

	def get_manual(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:MANual \n
		Snippet: value: float = driver.source.frequency.get_manual() \n
		Sets the frequency and triggers a sweep step manually if SWEep:MODE MAN. \n
			:return: manual: float You can select any frequency within the setting range, where: STARt is set with method RsSmab.Source.Frequency.start STOP is set with method RsSmab.Source.Frequency.stop OFFSet is set with method RsSmab.Source.Frequency.offset Range: (STARt + OFFSet) to (STOP + OFFSet) , Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MANual?')
		return Conversions.str_to_float(response)

	def set_manual(self, manual: float) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:MANual \n
		Snippet: driver.source.frequency.set_manual(manual = 1.0) \n
		Sets the frequency and triggers a sweep step manually if SWEep:MODE MAN. \n
			:param manual: float You can select any frequency within the setting range, where: STARt is set with method RsSmab.Source.Frequency.start STOP is set with method RsSmab.Source.Frequency.stop OFFSet is set with method RsSmab.Source.Frequency.offset Range: (STARt + OFFSet) to (STOP + OFFSet) , Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(manual)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:MANual {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FreqMode:
		"""SCPI: [SOURce<HW>]:FREQuency:MODE \n
		Snippet: value: enums.FreqMode = driver.source.frequency.get_mode() \n
		Sets the frequency mode for generating the RF output signal. The selected mode determines the parameters to be used for
		further frequency settings. \n
			:return: mode: CW| FIXed | SWEep| LIST CW|FIXed Sets the fixed frequency mode. CW and FIXed are synonyms. The instrument operates at a defined frequency, set with command [:​SOURcehw]:​FREQuency[:​CW|FIXed]. SWEep Sets sweep mode. The instrument processes frequency (and level) settings in defined sweep steps. Set the range and current frequency with the commands: method RsSmab.Source.Frequency.start and method RsSmab.Source.Frequency.stop, method RsSmab.Source.Frequency.center, method RsSmab.Source.Frequency.span, method RsSmab.Source.Frequency.manual LIST Sets list mode. The instrument processes frequency and level settings by means of values loaded from a list. To configure list mode settings, use the commands of the 'SOURce:LIST Subsystem'.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FreqMode)

	def set_mode(self, mode: enums.FreqMode) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:MODE \n
		Snippet: driver.source.frequency.set_mode(mode = enums.FreqMode.CW) \n
		Sets the frequency mode for generating the RF output signal. The selected mode determines the parameters to be used for
		further frequency settings. \n
			:param mode: CW| FIXed | SWEep| LIST CW|FIXed Sets the fixed frequency mode. CW and FIXed are synonyms. The instrument operates at a defined frequency, set with command [:​SOURcehw]:​FREQuency[:​CW|FIXed]. SWEep Sets sweep mode. The instrument processes frequency (and level) settings in defined sweep steps. Set the range and current frequency with the commands: method RsSmab.Source.Frequency.start and method RsSmab.Source.Frequency.stop, method RsSmab.Source.Frequency.center, method RsSmab.Source.Frequency.span, method RsSmab.Source.Frequency.manual LIST Sets list mode. The instrument processes frequency and level settings by means of values loaded from a list. To configure list mode settings, use the commands of the 'SOURce:LIST Subsystem'.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FreqMode)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:MODE {param}')

	def get_offset(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:OFFSet \n
		Snippet: value: float = driver.source.frequency.get_offset() \n
		Sets the frequency offset fFREQ:OFFSet of a downstream instrument. The parameters offset fFREQ:OFFSer and multiplier
		NFREQ:MULT affect the frequency value set with the command [:​SOURce<hw>]:​FREQuency[:​CW|FIXed].
		The query [:​SOURce<hw>]:​FREQuency[:​CW|FIXed] returns the value corresponding to the formula: fFREQ = fRFout *
		NFREQ:MULT + fFREQ:OFFSer See 'RF frequency and level display with a downstream instrument'. Note: The offset also
		affects RF frequency sweep. \n
			:return: offset: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, offset: float) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:OFFSet \n
		Snippet: driver.source.frequency.set_offset(offset = 1.0) \n
		Sets the frequency offset fFREQ:OFFSet of a downstream instrument. The parameters offset fFREQ:OFFSer and multiplier
		NFREQ:MULT affect the frequency value set with the command [:​SOURce<hw>]:​FREQuency[:​CW|FIXed].
		The query [:​SOURce<hw>]:​FREQuency[:​CW|FIXed] returns the value corresponding to the formula: fFREQ = fRFout *
		NFREQ:MULT + fFREQ:OFFSer See 'RF frequency and level display with a downstream instrument'. Note: The offset also
		affects RF frequency sweep. \n
			:param offset: float
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:OFFSet {param}')

	def get_span(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:SPAN \n
		Snippet: value: float = driver.source.frequency.get_span() \n
		Sets the sapn of the frequency sweep range. See 'Correlating Parameters in Sweep Mode'. \n
			:return: span: float Full freqeuncy range
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:SPAN?')
		return Conversions.str_to_float(response)

	def set_span(self, span: float) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:SPAN \n
		Snippet: driver.source.frequency.set_span(span = 1.0) \n
		Sets the sapn of the frequency sweep range. See 'Correlating Parameters in Sweep Mode'. \n
			:param span: float Full freqeuncy range
		"""
		param = Conversions.decimal_value_to_str(span)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:SPAN {param}')

	def get_start(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:STARt \n
		Snippet: value: float = driver.source.frequency.get_start() \n
		Sets the start frequency for the RF sweep. See 'Correlating Parameters in Sweep Mode'. \n
			:return: start: float Range: 300kHz to RFmax
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:STARt?')
		return Conversions.str_to_float(response)

	def set_start(self, start: float) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:STARt \n
		Snippet: driver.source.frequency.set_start(start = 1.0) \n
		Sets the start frequency for the RF sweep. See 'Correlating Parameters in Sweep Mode'. \n
			:param start: float Range: 300kHz to RFmax
		"""
		param = Conversions.decimal_value_to_str(start)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:STARt {param}')

	def get_stop(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:STOP \n
		Snippet: value: float = driver.source.frequency.get_stop() \n
		Sets the stop frequency range for the RF sweep. See 'Correlating Parameters in Sweep Mode'. \n
			:return: stop: float Range: 300kHz to RFmax, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:STOP?')
		return Conversions.str_to_float(response)

	def set_stop(self, stop: float) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:STOP \n
		Snippet: driver.source.frequency.set_stop(stop = 1.0) \n
		Sets the stop frequency range for the RF sweep. See 'Correlating Parameters in Sweep Mode'. \n
			:param stop: float Range: 300kHz to RFmax, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(stop)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:STOP {param}')

	def clone(self) -> 'Frequency':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frequency(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
