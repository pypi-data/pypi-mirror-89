from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Catalog:
	"""Catalog commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("catalog", core, parent)

	def get_source(self) -> List[str]:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:CATalog:SOURce \n
		Snippet: value: List[str] = driver.trigger.gprf.generator.arb.catalog.get_source() \n
		No command help available \n
			:return: trigger_sources: No help available
		"""
		response = self._core.io.query_str('TRIGger:GPRF:GENerator<Instance>:ARB:CATalog:SOURce?')
		return Conversions.str_to_str_list(response)
