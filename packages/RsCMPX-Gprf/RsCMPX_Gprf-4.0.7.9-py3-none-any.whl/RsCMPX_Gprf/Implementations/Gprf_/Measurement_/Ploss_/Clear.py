from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Clear:
	"""Clear commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("clear", core, parent)

	def initiate(self) -> None:
		"""SCPI: INITiate:GPRF:MEASurement<Instance>:PLOSs:CLEar \n
		Snippet: driver.gprf.measurement.ploss.clear.initiate() \n
		No command help available \n
		"""
		self._core.io.write(f'INITiate:GPRF:MEASurement<Instance>:PLOSs:CLEar')

	def initiate_with_opc(self) -> None:
		"""SCPI: INITiate:GPRF:MEASurement<Instance>:PLOSs:CLEar \n
		Snippet: driver.gprf.measurement.ploss.clear.initiate_with_opc() \n
		No command help available \n
		Same as initiate, but waits for the operation to complete before continuing further. Use the RsCMPX_Gprf.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'INITiate:GPRF:MEASurement<Instance>:PLOSs:CLEar')
