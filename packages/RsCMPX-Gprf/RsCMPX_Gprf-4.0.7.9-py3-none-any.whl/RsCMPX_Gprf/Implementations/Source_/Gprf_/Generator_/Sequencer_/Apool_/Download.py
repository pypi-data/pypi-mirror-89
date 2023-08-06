from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Download:
	"""Download commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("download", core, parent)

	def set(self) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:APOol:DOWNload \n
		Snippet: driver.source.gprf.generator.sequencer.apool.download.set() \n
		Downloads the ARB files from the file pool to the ARB RAM. \n
		"""
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:APOol:DOWNload')

	def set_with_opc(self) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:APOol:DOWNload \n
		Snippet: driver.source.gprf.generator.sequencer.apool.download.set_with_opc() \n
		Downloads the ARB files from the file pool to the ARB RAM. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCMPX_Gprf.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:APOol:DOWNload')
