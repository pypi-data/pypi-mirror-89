from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trace:
	"""Trace commands group definition. 8 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trace", core, parent)

	@property
	def magnitude(self):
		"""magnitude commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_magnitude'):
			from .Trace_.Magnitude import Magnitude
			self._magnitude = Magnitude(self._core, self._base)
		return self._magnitude

	@property
	def gdelay(self):
		"""gdelay commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gdelay'):
			from .Trace_.Gdelay import Gdelay
			self._gdelay = Gdelay(self._core, self._base)
		return self._gdelay

	def clone(self) -> 'Trace':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Trace(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
