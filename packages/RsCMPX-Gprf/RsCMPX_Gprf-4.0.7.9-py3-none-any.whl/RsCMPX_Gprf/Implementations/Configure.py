from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Configure:
	"""Configure commands group definition. 170 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("configure", core, parent)

	@property
	def gprf(self):
		"""gprf commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gprf'):
			from .Configure_.Gprf import Gprf
			self._gprf = Gprf(self._core, self._base)
		return self._gprf

	@property
	def tenvironment(self):
		"""tenvironment commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tenvironment'):
			from .Configure_.Tenvironment import Tenvironment
			self._tenvironment = Tenvironment(self._core, self._base)
		return self._tenvironment

	@property
	def system(self):
		"""system commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_system'):
			from .Configure_.System import System
			self._system = System(self._core, self._base)
		return self._system

	def clone(self) -> 'Configure':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Configure(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
