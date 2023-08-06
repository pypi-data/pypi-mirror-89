from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Update:
	"""Update commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("update", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:FIRMware:UPDate \n
		Snippet: driver.source.frequency.multiplier.external.firmware.update.set() \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:FIRMware:UPDate')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier:EXTernal:FIRMware:UPDate \n
		Snippet: driver.source.frequency.multiplier.external.firmware.update.set_with_opc() \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:FREQuency:MULTiplier:EXTernal:FIRMware:UPDate')
