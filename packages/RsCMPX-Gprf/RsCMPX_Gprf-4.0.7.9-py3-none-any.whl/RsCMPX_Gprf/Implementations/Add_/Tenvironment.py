from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tenvironment:
	"""Tenvironment commands group definition. 2 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tenvironment", core, parent)

	@property
	def spath(self):
		"""spath commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_spath'):
			from .Tenvironment_.Spath import Spath
			self._spath = Spath(self._core, self._base)
		return self._spath

	def clone(self) -> 'Tenvironment':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tenvironment(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
