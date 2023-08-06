from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Password:
	"""Password commands group definition. 4 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("password", core, parent)

	@property
	def cenable(self):
		"""cenable commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_cenable'):
			from .Password_.Cenable import Cenable
			self._cenable = Cenable(self._core, self._base)
		return self._cenable

	@property
	def new(self):
		"""new commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_new'):
			from .Password_.New import New
			self._new = New(self._core, self._base)
		return self._new

	def set_cdisable(self, usermode: enums.UserRole) -> None:
		"""SCPI: SYSTem:BASE:PASSword:CDISable \n
		Snippet: driver.system.password.set_cdisable(usermode = enums.UserRole.ADMin) \n
		No command help available \n
			:param usermode: No help available
		"""
		param = Conversions.enum_scalar_to_str(usermode, enums.UserRole)
		self._core.io.write(f'SYSTem:BASE:PASSword:CDISable {param}')

	def clone(self) -> 'Password':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Password(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
