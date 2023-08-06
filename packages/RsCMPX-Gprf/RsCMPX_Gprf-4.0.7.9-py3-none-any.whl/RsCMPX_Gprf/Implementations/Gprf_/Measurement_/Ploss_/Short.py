from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Short:
	"""Short commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("short", core, parent)

	# noinspection PyTypeChecker
	def fetch(self, connector: enums.CmwsConnector, path_index: enums.PathIndex = None) -> enums.PathLossState:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:PLOSs:SHORt \n
		Snippet: value: enums.PathLossState = driver.gprf.measurement.ploss.short.fetch(connector = enums.CmwsConnector.R11, path_index = enums.PathIndex.P1) \n
		No command help available \n
		Suppressed linked return values: reliability \n
			:param connector: No help available
			:param path_index: No help available
			:return: result_state_short: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('connector', connector, DataType.Enum), ArgSingle('path_index', path_index, DataType.Enum, True))
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:GPRF:MEASurement<Instance>:PLOSs:SHORt? {param}'.rstrip(), suppressed)
		return Conversions.str_to_scalar_enum(response, enums.PathLossState)
