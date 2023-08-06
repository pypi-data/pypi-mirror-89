from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Icomponent:
	"""Icomponent commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("icomponent", core, parent)

	def read(self) -> List[float]:
		"""SCPI: READ:GPRF:MEASurement<Instance>:IQVSlot:I \n
		Snippet: value: List[float] = driver.gprf.measurement.iqVsSlot.icomponent.read() \n
		Returns the contents of the I and Q result diagrams. \n
		Suppressed linked return values: reliability \n
			:return: idata: Comma-separated list of amplitudes, one value per measured step"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:GPRF:MEASurement<Instance>:IQVSlot:I?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:IQVSlot:I \n
		Snippet: value: List[float] = driver.gprf.measurement.iqVsSlot.icomponent.fetch() \n
		Returns the contents of the I and Q result diagrams. \n
		Suppressed linked return values: reliability \n
			:return: idata: Comma-separated list of amplitudes, one value per measured step"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GPRF:MEASurement<Instance>:IQVSlot:I?', suppressed)
		return response
