from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Corrected:
	"""Corrected commands group definition. 2 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("corrected", core, parent)

	@property
	def slot(self):
		"""slot commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_slot'):
			from .Corrected_.Slot import Slot
			self._slot = Slot(self._core, self._base)
		return self._slot

	def clone(self) -> 'Corrected':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Corrected(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
