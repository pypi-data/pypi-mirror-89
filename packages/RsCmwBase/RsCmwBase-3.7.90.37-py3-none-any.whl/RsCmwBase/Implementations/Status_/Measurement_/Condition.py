from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Condition:
	"""Condition commands group definition. 5 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("condition", core, parent)

	@property
	def off(self):
		"""off commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_off'):
			from .Condition_.Off import Off
			self._off = Off(self._core, self._base)
		return self._off

	@property
	def qued(self):
		"""qued commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_qued'):
			from .Condition_.Qued import Qued
			self._qued = Qued(self._core, self._base)
		return self._qued

	@property
	def run(self):
		"""run commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_run'):
			from .Condition_.Run import Run
			self._run = Run(self._core, self._base)
		return self._run

	@property
	def rdy(self):
		"""rdy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rdy'):
			from .Condition_.Rdy import Rdy
			self._rdy = Rdy(self._core, self._base)
		return self._rdy

	@property
	def sdReached(self):
		"""sdReached commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sdReached'):
			from .Condition_.SdReached import SdReached
			self._sdReached = SdReached(self._core, self._base)
		return self._sdReached

	def clone(self) -> 'Condition':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Condition(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
