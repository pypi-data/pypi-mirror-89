from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EnvelopePower:
	"""EnvelopePower commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("envelopePower", core, parent)

	def set(self, index: int, exp_nom_power: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQVSlot:LIST:ENPower \n
		Snippet: driver.configure.gprf.measurement.iqVsSlot.listPy.envelopePower.set(index = 1, exp_nom_power = 1.0) \n
		Defines or queries the expected nominal power of subsweep <Index>. \n
			:param index: No help available
			:param exp_nom_power: The range of the expected nominal power can be calculated as follows: Range (Expected Nominal Power) = Range (Input Power) + External Attenuation - User Margin The input power range is stated in the data sheet.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('index', index, DataType.Integer), ArgSingle('exp_nom_power', exp_nom_power, DataType.Float))
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQVSlot:LIST:ENPower {param}'.rstrip())

	def get(self, index: int) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQVSlot:LIST:ENPower \n
		Snippet: value: float = driver.configure.gprf.measurement.iqVsSlot.listPy.envelopePower.get(index = 1) \n
		Defines or queries the expected nominal power of subsweep <Index>. \n
			:param index: No help available
			:return: exp_nom_power: The range of the expected nominal power can be calculated as follows: Range (Expected Nominal Power) = Range (Input Power) + External Attenuation - User Margin The input power range is stated in the data sheet."""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'CONFigure:GPRF:MEASurement<Instance>:IQVSlot:LIST:ENPower? {param}')
		return Conversions.str_to_float(response)

	def get_all(self) -> List[float]:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQVSlot:LIST:ENPower:ALL \n
		Snippet: value: List[float] = driver.configure.gprf.measurement.iqVsSlot.listPy.envelopePower.get_all() \n
		Defines the expected nominal power for all subsweeps. \n
			:return: exp_nom_power: Comma-separated list of expected powers, one value per subsweep The range of the expected nominal power can be calculated as follows: Range (Expected Nominal Power) = Range (Input Power) + External Attenuation - User Margin The input power range is stated in the data sheet.
		"""
		response = self._core.io.query_bin_or_ascii_float_list('CONFigure:GPRF:MEASurement<Instance>:IQVSlot:LIST:ENPower:ALL?')
		return response

	def set_all(self, exp_nom_power: List[float]) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQVSlot:LIST:ENPower:ALL \n
		Snippet: driver.configure.gprf.measurement.iqVsSlot.listPy.envelopePower.set_all(exp_nom_power = [1.1, 2.2, 3.3]) \n
		Defines the expected nominal power for all subsweeps. \n
			:param exp_nom_power: Comma-separated list of expected powers, one value per subsweep The range of the expected nominal power can be calculated as follows: Range (Expected Nominal Power) = Range (Input Power) + External Attenuation - User Margin The input power range is stated in the data sheet.
		"""
		param = Conversions.list_to_csv_str(exp_nom_power)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQVSlot:LIST:ENPower:ALL {param}')
