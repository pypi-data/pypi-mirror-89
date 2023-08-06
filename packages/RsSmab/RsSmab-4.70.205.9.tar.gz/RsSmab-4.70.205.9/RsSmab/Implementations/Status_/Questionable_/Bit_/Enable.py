from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("enable", core, parent)

	def set(self, enable: str, bitNumber=repcap.BitNumber.Default) -> None:
		"""SCPI: STATus:QUEStionable:BIT<BITNR>:ENABle \n
		Snippet: driver.status.questionable.bit.enable.set(enable = '1', bitNumber = repcap.BitNumber.Default) \n
		No command help available \n
			:param enable: No help available
			:param bitNumber: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bit')"""
		param = Conversions.value_to_quoted_str(enable)
		bitNumber_cmd_val = self._base.get_repcap_cmd_value(bitNumber, repcap.BitNumber)
		self._core.io.write(f'STATus:QUEStionable:BIT{bitNumber_cmd_val}:ENABle {param}')

	def get(self, bitNumber=repcap.BitNumber.Default) -> str:
		"""SCPI: STATus:QUEStionable:BIT<BITNR>:ENABle \n
		Snippet: value: str = driver.status.questionable.bit.enable.get(bitNumber = repcap.BitNumber.Default) \n
		No command help available \n
			:param bitNumber: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bit')
			:return: enable: No help available"""
		bitNumber_cmd_val = self._base.get_repcap_cmd_value(bitNumber, repcap.BitNumber)
		response = self._core.io.query_str(f'STATus:QUEStionable:BIT{bitNumber_cmd_val}:ENABle?')
		return trim_str_response(response)
