from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Marker:
	"""Marker commands group definition. 3 total commands, 2 Sub-groups, 1 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("marker", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .Marker_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def fstate(self):
		"""fstate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fstate'):
			from .Marker_.Fstate import Fstate
			self._fstate = Fstate(self._core, self._base)
		return self._fstate

	# noinspection PyTypeChecker
	def get_active(self) -> enums.SweMarkActive:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:MARKer:ACTive \n
		Snippet: value: enums.SweMarkActive = driver.source.sweep.frequency.marker.get_active() \n
		Defines the marker signal to be output with a higher voltage than all other markers. \n
			:return: active: NONE| M01| M02| M03| M04| M05| M06| M07| M08| M09| M10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:FREQuency:MARKer:ACTive?')
		return Conversions.str_to_scalar_enum(response, enums.SweMarkActive)

	def set_active(self, active: enums.SweMarkActive) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:MARKer:ACTive \n
		Snippet: driver.source.sweep.frequency.marker.set_active(active = enums.SweMarkActive.M01) \n
		Defines the marker signal to be output with a higher voltage than all other markers. \n
			:param active: NONE| M01| M02| M03| M04| M05| M06| M07| M08| M09| M10
		"""
		param = Conversions.enum_scalar_to_str(active, enums.SweMarkActive)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:FREQuency:MARKer:ACTive {param}')

	def clone(self) -> 'Marker':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Marker(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
