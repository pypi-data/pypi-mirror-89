from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vbw:
	"""Vbw commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("vbw", core, parent)

	def get_auto(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:VBW:AUTO \n
		Snippet: value: bool = driver.configure.gprf.measurement.spectrum.zeroSpan.vbw.get_auto() \n
		No command help available \n
			:return: vbw_auto: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:VBW:AUTO?')
		return Conversions.str_to_bool(response)

	def set_auto(self, vbw_auto: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:VBW:AUTO \n
		Snippet: driver.configure.gprf.measurement.spectrum.zeroSpan.vbw.set_auto(vbw_auto = False) \n
		No command help available \n
			:param vbw_auto: No help available
		"""
		param = Conversions.bool_to_str(vbw_auto)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:VBW:AUTO {param}')

	def get_value(self) -> float or bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:VBW \n
		Snippet: value: float or bool = driver.configure.gprf.measurement.spectrum.zeroSpan.vbw.get_value() \n
		No command help available \n
			:return: vbw: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:VBW?')
		return Conversions.str_to_float_or_bool(response)

	def set_value(self, vbw: float or bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:VBW \n
		Snippet: driver.configure.gprf.measurement.spectrum.zeroSpan.vbw.set_value(vbw = 1.0) \n
		No command help available \n
			:param vbw: No help available
		"""
		param = Conversions.decimal_or_bool_value_to_str(vbw)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:VBW {param}')
