from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Help:
	"""Help commands group definition. 5 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("help", core, parent)

	@property
	def headers(self):
		"""headers commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_headers'):
			from .Help_.Headers import Headers
			self._headers = Headers(self._core, self._base)
		return self._headers

	@property
	def syntax(self):
		"""syntax commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_syntax'):
			from .Help_.Syntax import Syntax
			self._syntax = Syntax(self._core, self._base)
		return self._syntax

	@property
	def status(self):
		"""status commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_status'):
			from .Help_.Status import Status
			self._status = Status(self._core, self._base)
		return self._status

	def clone(self) -> 'Help':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Help(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
