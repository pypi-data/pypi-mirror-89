from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tenvironment:
	"""Tenvironment commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tenvironment", core, parent)

	@property
	def connectors(self):
		"""connectors commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_connectors'):
			from .Tenvironment_.Connectors import Connectors
			self._connectors = Connectors(self._core, self._base)
		return self._connectors

	def get_spath(self) -> List[str]:
		"""SCPI: CATalog:TENVironment:SPATh \n
		Snippet: value: List[str] = driver.catalog.tenvironment.get_spath() \n
		No command help available \n
			:return: name_signal_path: No help available
		"""
		response = self._core.io.query_str('CATalog:TENVironment:SPATh?')
		return Conversions.str_to_str_list(response)

	def clone(self) -> 'Tenvironment':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tenvironment(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
