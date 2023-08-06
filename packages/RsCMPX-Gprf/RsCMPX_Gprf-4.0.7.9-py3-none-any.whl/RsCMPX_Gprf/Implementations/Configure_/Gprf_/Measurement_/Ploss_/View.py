from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class View:
	"""View commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("view", core, parent)

	def get_aftaps(self) -> int:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:PLOSs:VIEW:AFTaps \n
		Snippet: value: int = driver.configure.gprf.measurement.ploss.view.get_aftaps() \n
		No command help available \n
			:return: avg_filter_taps: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:PLOSs:VIEW:AFTaps?')
		return Conversions.str_to_int(response)

	def set_aftaps(self, avg_filter_taps: int) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:PLOSs:VIEW:AFTaps \n
		Snippet: driver.configure.gprf.measurement.ploss.view.set_aftaps(avg_filter_taps = 1) \n
		No command help available \n
			:param avg_filter_taps: No help available
		"""
		param = Conversions.decimal_value_to_str(avg_filter_taps)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:PLOSs:VIEW:AFTaps {param}')
