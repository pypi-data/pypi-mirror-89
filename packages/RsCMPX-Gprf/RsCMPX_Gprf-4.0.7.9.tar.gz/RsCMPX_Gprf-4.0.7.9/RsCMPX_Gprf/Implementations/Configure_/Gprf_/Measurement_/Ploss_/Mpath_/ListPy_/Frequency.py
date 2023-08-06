from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def set(self, connector: enums.CmwsConnector, path_index: enums.PathIndex, num_entries: int, frequency: List[float]) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:PLOSs:MPATh:LIST:FREQuency \n
		Snippet: driver.configure.gprf.measurement.ploss.mpath.listPy.frequency.set(connector = enums.CmwsConnector.R11, path_index = enums.PathIndex.P1, num_entries = 1, frequency = [1.1, 2.2, 3.3]) \n
		No command help available \n
			:param connector: No help available
			:param path_index: No help available
			:param num_entries: No help available
			:param frequency: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('connector', connector, DataType.Enum), ArgSingle('path_index', path_index, DataType.Enum), ArgSingle('num_entries', num_entries, DataType.Integer), ArgSingle.as_open_list('frequency', frequency, DataType.FloatList))
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:PLOSs:MPATh:LIST:FREQuency {param}'.rstrip())

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Num_Entries: int: No parameter help available
			- Frequency: List[float]: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Num_Entries'),
			ArgStruct('Frequency', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Num_Entries: int = None
			self.Frequency: List[float] = None

	def get(self, connector: enums.CmwsConnector, path_index: enums.PathIndex) -> GetStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:PLOSs:MPATh:LIST:FREQuency \n
		Snippet: value: GetStruct = driver.configure.gprf.measurement.ploss.mpath.listPy.frequency.get(connector = enums.CmwsConnector.R11, path_index = enums.PathIndex.P1) \n
		No command help available \n
			:param connector: No help available
			:param path_index: No help available
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('connector', connector, DataType.Enum), ArgSingle('path_index', path_index, DataType.Enum))
		return self._core.io.query_struct(f'CONFigure:GPRF:MEASurement<Instance>:PLOSs:MPATh:LIST:FREQuency? {param}'.rstrip(), self.__class__.GetStruct())
