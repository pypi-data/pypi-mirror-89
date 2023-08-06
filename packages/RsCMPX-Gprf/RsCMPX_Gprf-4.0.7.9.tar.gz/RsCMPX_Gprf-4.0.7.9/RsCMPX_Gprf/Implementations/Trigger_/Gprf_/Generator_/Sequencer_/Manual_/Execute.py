from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Execute:
	"""Execute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("execute", core, parent)

	def set(self) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:SEQuencer:MANual:EXECute \n
		Snippet: driver.trigger.gprf.generator.sequencer.manual.execute.set() \n
		Triggers the transition to the next sequencer list entry manually. \n
		"""
		self._core.io.write(f'TRIGger:GPRF:GENerator<Instance>:SEQuencer:MANual:EXECute')

	def set_with_opc(self) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:SEQuencer:MANual:EXECute \n
		Snippet: driver.trigger.gprf.generator.sequencer.manual.execute.set_with_opc() \n
		Triggers the transition to the next sequencer list entry manually. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCMPX_Gprf.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'TRIGger:GPRF:GENerator<Instance>:SEQuencer:MANual:EXECute')
