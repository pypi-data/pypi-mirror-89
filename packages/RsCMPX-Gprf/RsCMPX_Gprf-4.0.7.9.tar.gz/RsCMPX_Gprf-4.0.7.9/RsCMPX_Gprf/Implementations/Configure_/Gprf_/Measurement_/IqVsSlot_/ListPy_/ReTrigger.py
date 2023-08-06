from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReTrigger:
	"""ReTrigger commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("reTrigger", core, parent)

	def set(self, index: int, retrigger: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQVSlot:LIST:RETRigger \n
		Snippet: driver.configure.gprf.measurement.iqVsSlot.listPy.reTrigger.set(index = 1, retrigger = False) \n
		Configures the retrigger mechanism for subsweep <Index>. The setting is only relevant for trigger mode Retrigger
		Preselect. \n
			:param index: No help available
			:param retrigger: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('index', index, DataType.Integer), ArgSingle('retrigger', retrigger, DataType.Boolean))
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQVSlot:LIST:RETRigger {param}'.rstrip())

	def get(self, index: int) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQVSlot:LIST:RETRigger \n
		Snippet: value: bool = driver.configure.gprf.measurement.iqVsSlot.listPy.reTrigger.get(index = 1) \n
		Configures the retrigger mechanism for subsweep <Index>. The setting is only relevant for trigger mode Retrigger
		Preselect. \n
			:param index: No help available
			:return: retrigger: No help available"""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'CONFigure:GPRF:MEASurement<Instance>:IQVSlot:LIST:RETRigger? {param}')
		return Conversions.str_to_bool(response)

	def get_all(self) -> List[bool]:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQVSlot:LIST:RETRigger:ALL \n
		Snippet: value: List[bool] = driver.configure.gprf.measurement.iqVsSlot.listPy.reTrigger.get_all() \n
		Configures the retrigger mechanism for all subsweeps. The setting is only relevant for trigger mode Retrigger Preselect. \n
			:return: retrigger: Comma-separated list of values, one value per subsweep
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQVSlot:LIST:RETRigger:ALL?')
		return Conversions.str_to_bool_list(response)

	def set_all(self, retrigger: List[bool]) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQVSlot:LIST:RETRigger:ALL \n
		Snippet: driver.configure.gprf.measurement.iqVsSlot.listPy.reTrigger.set_all(retrigger = [True, False, True]) \n
		Configures the retrigger mechanism for all subsweeps. The setting is only relevant for trigger mode Retrigger Preselect. \n
			:param retrigger: Comma-separated list of values, one value per subsweep
		"""
		param = Conversions.list_to_csv_str(retrigger)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQVSlot:LIST:RETRigger:ALL {param}')
