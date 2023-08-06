from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Attenuation:
	"""Attenuation commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("attenuation", core, parent)

	def get_state(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:ATTenuation:STATe \n
		Snippet: value: bool = driver.configure.gprf.measurement.extPwrSensor.attenuation.get_state() \n
		Enables or disables the result correction for an external input attenuation. \n
			:return: attenuat_state: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:EPSensor:ATTenuation:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, attenuat_state: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:ATTenuation:STATe \n
		Snippet: driver.configure.gprf.measurement.extPwrSensor.attenuation.set_state(attenuat_state = False) \n
		Enables or disables the result correction for an external input attenuation. \n
			:param attenuat_state: No help available
		"""
		param = Conversions.bool_to_str(attenuat_state)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:EPSensor:ATTenuation:STATe {param}')

	def get_value(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:ATTenuation \n
		Snippet: value: float = driver.configure.gprf.measurement.extPwrSensor.attenuation.get_value() \n
		Specifies an external input attenuation factor for correction of the power results. \n
			:return: attenuation: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:EPSensor:ATTenuation?')
		return Conversions.str_to_float(response)

	def set_value(self, attenuation: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:ATTenuation \n
		Snippet: driver.configure.gprf.measurement.extPwrSensor.attenuation.set_value(attenuation = 1.0) \n
		Specifies an external input attenuation factor for correction of the power results. \n
			:param attenuation: No help available
		"""
		param = Conversions.decimal_value_to_str(attenuation)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:EPSensor:ATTenuation {param}')
