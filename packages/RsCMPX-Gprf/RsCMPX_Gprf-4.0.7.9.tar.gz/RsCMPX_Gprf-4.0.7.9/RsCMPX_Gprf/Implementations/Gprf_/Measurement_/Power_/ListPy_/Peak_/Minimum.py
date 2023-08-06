from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Minimum:
	"""Minimum commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("minimum", core, parent)

	def calculate(self, list_index: int) -> List[float]:
		"""SCPI: CALCulate:GPRF:MEASurement<Instance>:POWer:LIST:PEAK:MINimum \n
		Snippet: value: List[float] = driver.gprf.measurement.power.listPy.peak.minimum.calculate(list_index = 1) \n
		Returns power results for segment <ListIndex>, see 'Results in List Mode'.
			INTRO_CMD_HELP: The following powers can be retrieved: \n
			- Current RMS (...:LIST:CURRent?)
			- Current Min. (...:MINimum:CURRent?)
			- Current Max. (...:MAXimum:CURRent?)
			- Average RMS (...:AVERage?)
			- Minimum (...:PEAK:MINimum?)
			- Maximum (...:PEAK:MAXimum?)
			- Standard Deviation (...:SDEViation?)
		The values described below are returned by FETCh and READ commands. CALCulate commands return error codes instead, one
		value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:param list_index: Index of the segment
			:return: power_minimum_min: Power value for the selected segment"""
		param = Conversions.decimal_value_to_str(list_index)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'CALCulate:GPRF:MEASurement<Instance>:POWer:LIST:PEAK:MINimum? {param}', suppressed)
		return response

	def fetch(self, list_index: int) -> List[float]:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:POWer:LIST:PEAK:MINimum \n
		Snippet: value: List[float] = driver.gprf.measurement.power.listPy.peak.minimum.fetch(list_index = 1) \n
		Returns power results for segment <ListIndex>, see 'Results in List Mode'.
			INTRO_CMD_HELP: The following powers can be retrieved: \n
			- Current RMS (...:LIST:CURRent?)
			- Current Min. (...:MINimum:CURRent?)
			- Current Max. (...:MAXimum:CURRent?)
			- Average RMS (...:AVERage?)
			- Minimum (...:PEAK:MINimum?)
			- Maximum (...:PEAK:MAXimum?)
			- Standard Deviation (...:SDEViation?)
		The values described below are returned by FETCh and READ commands. CALCulate commands return error codes instead, one
		value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:param list_index: Index of the segment
			:return: power_minimum_min: Power value for the selected segment"""
		param = Conversions.decimal_value_to_str(list_index)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GPRF:MEASurement<Instance>:POWer:LIST:PEAK:MINimum? {param}', suppressed)
		return response

	def read(self, list_index: int) -> List[float]:
		"""SCPI: READ:GPRF:MEASurement<Instance>:POWer:LIST:PEAK:MINimum \n
		Snippet: value: List[float] = driver.gprf.measurement.power.listPy.peak.minimum.read(list_index = 1) \n
		Returns power results for segment <ListIndex>, see 'Results in List Mode'.
			INTRO_CMD_HELP: The following powers can be retrieved: \n
			- Current RMS (...:LIST:CURRent?)
			- Current Min. (...:MINimum:CURRent?)
			- Current Max. (...:MAXimum:CURRent?)
			- Average RMS (...:AVERage?)
			- Minimum (...:PEAK:MINimum?)
			- Maximum (...:PEAK:MAXimum?)
			- Standard Deviation (...:SDEViation?)
		The values described below are returned by FETCh and READ commands. CALCulate commands return error codes instead, one
		value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:param list_index: Index of the segment
			:return: power_minimum_min: Power value for the selected segment"""
		param = Conversions.decimal_value_to_str(list_index)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:GPRF:MEASurement<Instance>:POWer:LIST:PEAK:MINimum? {param}', suppressed)
		return response
