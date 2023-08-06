from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CorrectionTable:
	"""CorrectionTable commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("correctionTable", core, parent)

	def set(self, name: str, frequency: List[float], attenuation: List[float]) -> None:
		"""SCPI: MODify:SYSTem:ATTenuation:CTABle \n
		Snippet: driver.modify.system.attenuation.correctionTable.set(name = '1', frequency = [1.1, 2.2, 3.3], attenuation = [1.1, 2.2, 3.3]) \n
		No command help available \n
			:param name: No help available
			:param frequency: No help available
			:param attenuation: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('name', name, DataType.String), ArgSingle.as_open_list('frequency', frequency, DataType.FloatList), ArgSingle.as_open_list('attenuation', attenuation, DataType.FloatList))
		self._core.io.write(f'MODify:SYSTem:ATTenuation:CTABle {param}'.rstrip())
