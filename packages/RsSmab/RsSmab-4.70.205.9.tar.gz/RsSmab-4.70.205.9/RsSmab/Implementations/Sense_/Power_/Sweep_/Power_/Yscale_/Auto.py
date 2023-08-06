from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Auto:
	"""Auto commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("auto", core, parent)

	def reset(self) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:POWer:YSCale:AUTO:RESet \n
		Snippet: driver.sense.power.sweep.power.yscale.auto.reset() \n
		Resets the Y scale to suitable values after the use of auto scaling in the expanding mode. For this mode, the scale might
		get expanded because of temporarily high power values. The reset function allows resetting the diagram to match smaller
		power values again. \n
		"""
		self._core.io.write(f'SENSe:POWer:SWEep:POWer:YSCale:AUTO:RESet')

	def reset_with_opc(self) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:POWer:YSCale:AUTO:RESet \n
		Snippet: driver.sense.power.sweep.power.yscale.auto.reset_with_opc() \n
		Resets the Y scale to suitable values after the use of auto scaling in the expanding mode. For this mode, the scale might
		get expanded because of temporarily high power values. The reset function allows resetting the diagram to match smaller
		power values again. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SENSe:POWer:SWEep:POWer:YSCale:AUTO:RESet')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.MeasRespYsCaleMode:
		"""SCPI: SENSe:[POWer]:SWEep:POWer:YSCale:AUTO \n
		Snippet: value: enums.MeasRespYsCaleMode = driver.sense.power.sweep.power.yscale.auto.get_value() \n
		Activates autoscaling of the Y axis of the diagram. \n
			:return: auto: OFF| CEXPanding| FEXPanding| CFLoating| FFLoating OFF Auto scaling is deactivated. When switching from activated to deactivated Auto scaling, the scaling is maintained. When switching from deactivated to activated Auto scaling, the scaling is reset to min = max = 0. CEXPanding | FEXPanding Auto scale is activated. The scaling of the Y-axis is selected in such a way, that the trace is always visible. To this end, the range is expanded if the minimum or maximum values of the trace move outside the current scale. The step width is 5 dB for selection course and variable in the range of 0.2 db to 5 dB for selection fine. CFLoating | FFLoating Auto scale is activated. The scaling of the Y-axis is selected in such a way, that the trace is always visible. To this end, the range is either expanded if the minimum or maximum values of the trace move outside the current scale or scaled down if the trace fits into a reduced scale. The step width is 5 dB for selection course and variable in the range of 0.2 db to 5 dB for selection fine.
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:POWer:YSCale:AUTO?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespYsCaleMode)

	def set_value(self, auto: enums.MeasRespYsCaleMode) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:POWer:YSCale:AUTO \n
		Snippet: driver.sense.power.sweep.power.yscale.auto.set_value(auto = enums.MeasRespYsCaleMode.CEXPanding) \n
		Activates autoscaling of the Y axis of the diagram. \n
			:param auto: OFF| CEXPanding| FEXPanding| CFLoating| FFLoating OFF Auto scaling is deactivated. When switching from activated to deactivated Auto scaling, the scaling is maintained. When switching from deactivated to activated Auto scaling, the scaling is reset to min = max = 0. CEXPanding | FEXPanding Auto scale is activated. The scaling of the Y-axis is selected in such a way, that the trace is always visible. To this end, the range is expanded if the minimum or maximum values of the trace move outside the current scale. The step width is 5 dB for selection course and variable in the range of 0.2 db to 5 dB for selection fine. CFLoating | FFLoating Auto scale is activated. The scaling of the Y-axis is selected in such a way, that the trace is always visible. To this end, the range is either expanded if the minimum or maximum values of the trace move outside the current scale or scaled down if the trace fits into a reduced scale. The step width is 5 dB for selection course and variable in the range of 0.2 db to 5 dB for selection fine.
		"""
		param = Conversions.enum_scalar_to_str(auto, enums.MeasRespYsCaleMode)
		self._core.io.write(f'SENSe:POWer:SWEep:POWer:YSCale:AUTO {param}')
