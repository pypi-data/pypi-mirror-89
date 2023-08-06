from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dtime:
	"""Dtime commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dtime", core, parent)

	def set(self, index: int, dwell_time: float) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:DTIMe \n
		Snippet: driver.source.gprf.generator.sequencer.listPy.dtime.set(index = 1, dwell_time = 1.0) \n
		Defines or queries the dwell time for the sequencer list entry with the selected <Index>. \n
			:param index: No help available
			:param dwell_time: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('index', index, DataType.Integer), ArgSingle('dwell_time', dwell_time, DataType.Float))
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:DTIMe {param}'.rstrip())

	def get(self, index: int) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:DTIMe \n
		Snippet: value: float = driver.source.gprf.generator.sequencer.listPy.dtime.get(index = 1) \n
		Defines or queries the dwell time for the sequencer list entry with the selected <Index>. \n
			:param index: No help available
			:return: dwell_time: No help available"""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:DTIMe? {param}')
		return Conversions.str_to_float(response)

	def get_all(self) -> List[float]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:DTIMe:ALL \n
		Snippet: value: List[float] = driver.source.gprf.generator.sequencer.listPy.dtime.get_all() \n
		Defines the dwell times for all sequencer list entries. \n
			:return: dwell_time: Comma-separated list of values, one value per list entry
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:DTIMe:ALL?')
		return response

	def set_all(self, dwell_time: List[float]) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:DTIMe:ALL \n
		Snippet: driver.source.gprf.generator.sequencer.listPy.dtime.set_all(dwell_time = [1.1, 2.2, 3.3]) \n
		Defines the dwell times for all sequencer list entries. \n
			:param dwell_time: Comma-separated list of values, one value per list entry
		"""
		param = Conversions.list_to_csv_str(dwell_time)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:DTIMe:ALL {param}')
