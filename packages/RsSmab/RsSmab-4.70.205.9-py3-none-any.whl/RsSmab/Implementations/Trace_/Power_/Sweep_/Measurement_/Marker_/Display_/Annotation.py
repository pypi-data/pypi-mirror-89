from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Annotation:
	"""Annotation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("annotation", core, parent)

	def get_state(self) -> bool:
		"""SCPI: TRACe:[POWer]:SWEep:MEASurement:MARKer:DISPlay:ANNotation:[STATe] \n
		Snippet: value: bool = driver.trace.power.sweep.measurement.marker.display.annotation.get_state() \n
		Activates the indication of the markers and the marker list in the measurement diagram and in the hardcopy file. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('TRACe:POWer:SWEep:MEASurement:MARKer:DISPlay:ANNotation:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: TRACe:[POWer]:SWEep:MEASurement:MARKer:DISPlay:ANNotation:[STATe] \n
		Snippet: driver.trace.power.sweep.measurement.marker.display.annotation.set_state(state = False) \n
		Activates the indication of the markers and the marker list in the measurement diagram and in the hardcopy file. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'TRACe:POWer:SWEep:MEASurement:MARKer:DISPlay:ANNotation:STATe {param}')
