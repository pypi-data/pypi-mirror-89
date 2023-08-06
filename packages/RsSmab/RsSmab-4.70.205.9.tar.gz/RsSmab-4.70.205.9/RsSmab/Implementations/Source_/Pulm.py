from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pulm:
	"""Pulm commands group definition. 46 total commands, 4 Sub-groups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pulm", core, parent)

	@property
	def double(self):
		"""double commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_double'):
			from .Pulm_.Double import Double
			self._double = Double(self._core, self._base)
		return self._double

	@property
	def train(self):
		"""train commands group. 5 Sub-classes, 3 commands."""
		if not hasattr(self, '_train'):
			from .Pulm_.Train import Train
			self._train = Train(self._core, self._base)
		return self._train

	@property
	def trigger(self):
		"""trigger commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_trigger'):
			from .Pulm_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def internal(self):
		"""internal commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_internal'):
			from .Pulm_.Internal import Internal
			self._internal = Internal(self._core, self._base)
		return self._internal

	def get_delay(self) -> float:
		"""SCPI: [SOURce<HW>]:PULM:DELay \n
		Snippet: value: float = driver.source.pulm.get_delay() \n
		Sets the pulse delay. \n
			:return: delay: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""SCPI: [SOURce<HW>]:PULM:DELay \n
		Snippet: driver.source.pulm.set_delay(delay = 1.0) \n
		Sets the pulse delay. \n
			:param delay: float
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:PULM:DELay {param}')

	# noinspection PyTypeChecker
	def get_impedance(self) -> enums.InpImpRf:
		"""SCPI: [SOURce<HW>]:PULM:IMPedance \n
		Snippet: value: enums.InpImpRf = driver.source.pulm.get_impedance() \n
		Sets the impedance for the external pulse trigger and pulse modulation input. \n
			:return: impedance: G50| G10K
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:IMPedance?')
		return Conversions.str_to_scalar_enum(response, enums.InpImpRf)

	def set_impedance(self, impedance: enums.InpImpRf) -> None:
		"""SCPI: [SOURce<HW>]:PULM:IMPedance \n
		Snippet: driver.source.pulm.set_impedance(impedance = enums.InpImpRf.G10K) \n
		Sets the impedance for the external pulse trigger and pulse modulation input. \n
			:param impedance: G50| G10K
		"""
		param = Conversions.enum_scalar_to_str(impedance, enums.InpImpRf)
		self._core.io.write(f'SOURce<HwInstance>:PULM:IMPedance {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.PulsMode:
		"""SCPI: [SOURce<HW>]:PULM:MODE \n
		Snippet: value: enums.PulsMode = driver.source.pulm.get_mode() \n
		Selects the mode for the pulse modulation. \n
			:return: mode: SINGle| DOUBle | PTRain SINGle Generates a single pulse. DOUBle Generates two pulses within one pulse period. PTRain Generates a user-defined pulse train. Specify the pulse sequence with the commands: method RsSmab.Source.Pulm.Train.Ontime.value method RsSmab.Source.Pulm.Train.OffTime.value method RsSmab.Source.Pulm.Train.Repetition.value
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.PulsMode)

	def set_mode(self, mode: enums.PulsMode) -> None:
		"""SCPI: [SOURce<HW>]:PULM:MODE \n
		Snippet: driver.source.pulm.set_mode(mode = enums.PulsMode.DOUBle) \n
		Selects the mode for the pulse modulation. \n
			:param mode: SINGle| DOUBle | PTRain SINGle Generates a single pulse. DOUBle Generates two pulses within one pulse period. PTRain Generates a user-defined pulse train. Specify the pulse sequence with the commands: method RsSmab.Source.Pulm.Train.Ontime.value method RsSmab.Source.Pulm.Train.OffTime.value method RsSmab.Source.Pulm.Train.Repetition.value
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.PulsMode)
		self._core.io.write(f'SOURce<HwInstance>:PULM:MODE {param}')

	def get_period(self) -> float:
		"""SCPI: [SOURce<HW>]:PULM:PERiod \n
		Snippet: value: float = driver.source.pulm.get_period() \n
		Sets the period of the generated pulse, that means the repetition frequency of the internally generated modulation signal. \n
			:return: period: float The minimum value depends on the installed options R&S SMAB-K22 or R&S SMAB-K23 Range: 20E-9 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:PERiod?')
		return Conversions.str_to_float(response)

	def set_period(self, period: float) -> None:
		"""SCPI: [SOURce<HW>]:PULM:PERiod \n
		Snippet: driver.source.pulm.set_period(period = 1.0) \n
		Sets the period of the generated pulse, that means the repetition frequency of the internally generated modulation signal. \n
			:param period: float The minimum value depends on the installed options R&S SMAB-K22 or R&S SMAB-K23 Range: 20E-9 to 100
		"""
		param = Conversions.decimal_value_to_str(period)
		self._core.io.write(f'SOURce<HwInstance>:PULM:PERiod {param}')

	# noinspection PyTypeChecker
	def get_polarity(self) -> enums.NormInv:
		"""SCPI: [SOURce<HW>]:PULM:POLarity \n
		Snippet: value: enums.NormInv = driver.source.pulm.get_polarity() \n
		Sets the polarity of the externally applied modulation signal. \n
			:return: polarity: NORMal| INVerted NORMal Suppresses the RF signal during the pulse pause. INVerted Suppresses the RF signal during the pulse.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:POLarity?')
		return Conversions.str_to_scalar_enum(response, enums.NormInv)

	def set_polarity(self, polarity: enums.NormInv) -> None:
		"""SCPI: [SOURce<HW>]:PULM:POLarity \n
		Snippet: driver.source.pulm.set_polarity(polarity = enums.NormInv.INVerted) \n
		Sets the polarity of the externally applied modulation signal. \n
			:param polarity: NORMal| INVerted NORMal Suppresses the RF signal during the pulse pause. INVerted Suppresses the RF signal during the pulse.
		"""
		param = Conversions.enum_scalar_to_str(polarity, enums.NormInv)
		self._core.io.write(f'SOURce<HwInstance>:PULM:POLarity {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.SourceInt:
		"""SCPI: [SOURce<HW>]:PULM:SOURce \n
		Snippet: value: enums.SourceInt = driver.source.pulm.get_source() \n
		Selects between the internal (pulse generator) or an external pulse signal for the modulation. \n
			:return: source: INTernal| EXTernal
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SourceInt)

	def set_source(self, source: enums.SourceInt) -> None:
		"""SCPI: [SOURce<HW>]:PULM:SOURce \n
		Snippet: driver.source.pulm.set_source(source = enums.SourceInt.EXTernal) \n
		Selects between the internal (pulse generator) or an external pulse signal for the modulation. \n
			:param source: INTernal| EXTernal
		"""
		param = Conversions.enum_scalar_to_str(source, enums.SourceInt)
		self._core.io.write(f'SOURce<HwInstance>:PULM:SOURce {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:PULM:STATe \n
		Snippet: value: bool = driver.source.pulm.get_state() \n
		Activates pulse modulation. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:PULM:STATe \n
		Snippet: driver.source.pulm.set_state(state = False) \n
		Activates pulse modulation. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:PULM:STATe {param}')

	def get_threshold(self) -> float:
		"""SCPI: [SOURce<HW>]:PULM:THReshold \n
		Snippet: value: float = driver.source.pulm.get_threshold() \n
		Sets the threshold for the input signal at the [Pulse Ext] connector. \n
			:return: threshold: float Range: 0 to 2, Unit: V
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:THReshold?')
		return Conversions.str_to_float(response)

	def set_threshold(self, threshold: float) -> None:
		"""SCPI: [SOURce<HW>]:PULM:THReshold \n
		Snippet: driver.source.pulm.set_threshold(threshold = 1.0) \n
		Sets the threshold for the input signal at the [Pulse Ext] connector. \n
			:param threshold: float Range: 0 to 2, Unit: V
		"""
		param = Conversions.decimal_value_to_str(threshold)
		self._core.io.write(f'SOURce<HwInstance>:PULM:THReshold {param}')

	# noinspection PyTypeChecker
	def get_ttype(self) -> enums.PulsTransType:
		"""SCPI: [SOURce<HW>]:PULM:TTYPe \n
		Snippet: value: enums.PulsTransType = driver.source.pulm.get_ttype() \n
		Sets the transition mode for the pulse signal. \n
			:return: source: SMOothed| FAST SMOothed flattens the slew rate, resulting in longer rise/fall times. FAST enables fast transitions with shortest rise and fall times.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:TTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.PulsTransType)

	def set_ttype(self, source: enums.PulsTransType) -> None:
		"""SCPI: [SOURce<HW>]:PULM:TTYPe \n
		Snippet: driver.source.pulm.set_ttype(source = enums.PulsTransType.FAST) \n
		Sets the transition mode for the pulse signal. \n
			:param source: SMOothed| FAST SMOothed flattens the slew rate, resulting in longer rise/fall times. FAST enables fast transitions with shortest rise and fall times.
		"""
		param = Conversions.enum_scalar_to_str(source, enums.PulsTransType)
		self._core.io.write(f'SOURce<HwInstance>:PULM:TTYPe {param}')

	def get_width(self) -> float:
		"""SCPI: [SOURce<HW>]:PULM:WIDTh \n
		Snippet: value: float = driver.source.pulm.get_width() \n
		Sets the width of the generated pulse, that means the pulse length. It must be at least 20ns less than the set pulse
		period. \n
			:return: width: float Range: 20E-9 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:WIDTh?')
		return Conversions.str_to_float(response)

	def set_width(self, width: float) -> None:
		"""SCPI: [SOURce<HW>]:PULM:WIDTh \n
		Snippet: driver.source.pulm.set_width(width = 1.0) \n
		Sets the width of the generated pulse, that means the pulse length. It must be at least 20ns less than the set pulse
		period. \n
			:param width: float Range: 20E-9 to 100
		"""
		param = Conversions.decimal_value_to_str(width)
		self._core.io.write(f'SOURce<HwInstance>:PULM:WIDTh {param}')

	def clone(self) -> 'Pulm':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pulm(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
