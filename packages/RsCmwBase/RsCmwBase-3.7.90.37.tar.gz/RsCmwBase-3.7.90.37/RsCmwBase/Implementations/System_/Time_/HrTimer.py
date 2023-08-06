from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HrTimer:
	"""HrTimer commands group definition. 4 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hrTimer", core, parent)

	@property
	def absolute(self):
		"""absolute commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_absolute'):
			from .HrTimer_.Absolute import Absolute
			self._absolute = Absolute(self._core, self._base)
		return self._absolute

	def set_relative(self, duration: int) -> None:
		"""SCPI: SYSTem:TIME:HRTimer:RELative \n
		Snippet: driver.system.time.hrTimer.set_relative(duration = 1) \n
		This command starts a timer. After the specified timeout, an OPC is generated. When the timer expires, 'Operation
		Complete' is indicated. This event can be evaluated by polling, via a *OPC? or via *WAI. \n
			:param duration: Range: 0 ms to 4294967295 ms, Unit: ms
		"""
		param = Conversions.decimal_value_to_str(duration)
		self._core.io.write_with_opc(f'SYSTem:TIME:HRTimer:RELative {param}')

	def clone(self) -> 'HrTimer':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HrTimer(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
