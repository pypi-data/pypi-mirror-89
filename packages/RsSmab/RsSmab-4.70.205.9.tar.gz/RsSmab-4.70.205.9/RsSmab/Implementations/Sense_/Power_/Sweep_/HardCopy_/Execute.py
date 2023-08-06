from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Execute:
	"""Execute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("execute", core, parent)

	def set(self) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:[EXECute] \n
		Snippet: driver.sense.power.sweep.hardCopy.execute.set() \n
		Triggers the generation of a hardcopy of the current measurement diagram. The data is written into the file
		selected/created with the SWEep:HCOPy command. \n
		"""
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:EXECute')

	def set_with_opc(self) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:[EXECute] \n
		Snippet: driver.sense.power.sweep.hardCopy.execute.set_with_opc() \n
		Triggers the generation of a hardcopy of the current measurement diagram. The data is written into the file
		selected/created with the SWEep:HCOPy command. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SENSe:POWer:SWEep:HCOPy:EXECute')
