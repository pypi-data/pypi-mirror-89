from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def calculate(self) -> List[float]:
		"""SCPI: CALCulate:GPRF:MEASurement<Instance>:POWer:MINimum:CURRent \n
		Snippet: value: List[float] = driver.gprf.measurement.power.minimum.current.calculate() \n
		Returns power results for all segments, see 'Results in List Mode'.
			INTRO_CMD_HELP: The following results can be retrieved: \n
			- Current RMS (...:POWer:CURRent?)
			- Current Min. (...:MINimum:CURRent?)
			- Current Max. (...:MAXimum:CURRent?)
			- Average RMS (...:AVERage?)
			- Minimum (...:PEAK:MINimum?)
			- Maximum (...:PEAK:MAXimum?)
			- Standard Deviation (...:SDEViation?)
		The values described below are returned by FETCh and READ commands. CALCulate commands return error codes instead, one
		value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:return: power_current_min: Comma-separated list of power values, one value per measured segment"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'CALCulate:GPRF:MEASurement<Instance>:POWer:MINimum:CURRent?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:POWer:MINimum:CURRent \n
		Snippet: value: List[float] = driver.gprf.measurement.power.minimum.current.fetch() \n
		Returns power results for all segments, see 'Results in List Mode'.
			INTRO_CMD_HELP: The following results can be retrieved: \n
			- Current RMS (...:POWer:CURRent?)
			- Current Min. (...:MINimum:CURRent?)
			- Current Max. (...:MAXimum:CURRent?)
			- Average RMS (...:AVERage?)
			- Minimum (...:PEAK:MINimum?)
			- Maximum (...:PEAK:MAXimum?)
			- Standard Deviation (...:SDEViation?)
		The values described below are returned by FETCh and READ commands. CALCulate commands return error codes instead, one
		value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:return: power_current_min: Comma-separated list of power values, one value per measured segment"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GPRF:MEASurement<Instance>:POWer:MINimum:CURRent?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:GPRF:MEASurement<Instance>:POWer:MINimum:CURRent \n
		Snippet: value: List[float] = driver.gprf.measurement.power.minimum.current.read() \n
		Returns power results for all segments, see 'Results in List Mode'.
			INTRO_CMD_HELP: The following results can be retrieved: \n
			- Current RMS (...:POWer:CURRent?)
			- Current Min. (...:MINimum:CURRent?)
			- Current Max. (...:MAXimum:CURRent?)
			- Average RMS (...:AVERage?)
			- Minimum (...:PEAK:MINimum?)
			- Maximum (...:PEAK:MAXimum?)
			- Standard Deviation (...:SDEViation?)
		The values described below are returned by FETCh and READ commands. CALCulate commands return error codes instead, one
		value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:return: power_current_min: Comma-separated list of power values, one value per measured segment"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:GPRF:MEASurement<Instance>:POWer:MINimum:CURRent?', suppressed)
		return response
