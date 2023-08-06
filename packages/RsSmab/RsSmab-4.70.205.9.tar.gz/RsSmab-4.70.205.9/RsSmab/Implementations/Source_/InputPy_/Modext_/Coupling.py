from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Coupling:
	"""Coupling commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("coupling", core, parent)
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

	def set(self, coupling: enums.AcDc, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:INPut:MODext:COUPling<CH> \n
		Snippet: driver.source.inputPy.modext.coupling.set(coupling = enums.AcDc.AC, channel = repcap.Channel.Default) \n
		Selects the coupling mode for an externally applied modulation signal. \n
			:param coupling: AC| DC AC Passes the AC signal component of the modulation signal. DC Passes the modulation signal with both components, AC and DC. For active external exponential AM, automatically sets [:SOURcehw]:INPut:MODext:COUPlingchDC.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coupling')"""
		param = Conversions.enum_scalar_to_str(coupling, enums.AcDc)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:INPut:MODext:COUPling{channel_cmd_val} {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.AcDc:
		"""SCPI: [SOURce<HW>]:INPut:MODext:COUPling<CH> \n
		Snippet: value: enums.AcDc = driver.source.inputPy.modext.coupling.get(channel = repcap.Channel.Default) \n
		Selects the coupling mode for an externally applied modulation signal. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coupling')
			:return: coupling: AC| DC AC Passes the AC signal component of the modulation signal. DC Passes the modulation signal with both components, AC and DC. For active external exponential AM, automatically sets [:SOURcehw]:INPut:MODext:COUPlingchDC."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:INPut:MODext:COUPling{channel_cmd_val}?')
		return Conversions.str_to_scalar_enum(response, enums.AcDc)

	def clone(self) -> 'Coupling':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Coupling(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
