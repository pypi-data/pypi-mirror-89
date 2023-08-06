from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Monitor:
	"""Monitor commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("monitor", core, parent)

	@property
	def off(self):
		"""off commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_off'):
			from .Monitor_.Off import Off
			self._off = Off(self._core, self._base)
		return self._off

	def set_value(self, enable: bool) -> None:
		"""SCPI: SYSTem:DISPlay:MONitor \n
		Snippet: driver.system.display.monitor.set_value(enable = False) \n
		Turns the built-in display / the external monitor on or off. \n
			:param enable: ON | OFF
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'SYSTem:DISPlay:MONitor {param}')

	def clone(self) -> 'Monitor':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Monitor(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
