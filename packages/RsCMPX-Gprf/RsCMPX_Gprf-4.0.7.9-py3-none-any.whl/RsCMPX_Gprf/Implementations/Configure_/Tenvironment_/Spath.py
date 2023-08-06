from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Spath:
	"""Spath commands group definition. 4 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spath", core, parent)

	@property
	def info(self):
		"""info commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_info'):
			from .Spath_.Info import Info
			self._info = Info(self._core, self._base)
		return self._info

	@property
	def direction(self):
		"""direction commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_direction'):
			from .Spath_.Direction import Direction
			self._direction = Direction(self._core, self._base)
		return self._direction

	@property
	def correctionTable(self):
		"""correctionTable commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_correctionTable'):
			from .Spath_.CorrectionTable import CorrectionTable
			self._correctionTable = CorrectionTable(self._core, self._base)
		return self._correctionTable

	def clone(self) -> 'Spath':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Spath(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
