from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DaylightSavingTime:
	"""DaylightSavingTime commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("daylightSavingTime", core, parent)

	@property
	def rule(self):
		"""rule commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rule'):
			from .DaylightSavingTime_.Rule import Rule
			self._rule = Rule(self._core, self._base)
		return self._rule

	def get_mode(self) -> bool:
		"""SCPI: SYSTem:TIME:DSTime:MODE \n
		Snippet: value: bool = driver.system.time.daylightSavingTime.get_mode() \n
		Configures whether the operating system automatically adjusts its clock for daylight saving time (DST) or not. The rules
		defining when exactly the clock must be adjusted by which offset depend on the configured time zone, see method RsCmwBase.
		System.Time.DaylightSavingTime.Rule.value. If the automatism is disabled, the local time is calculated as: Local time =
		UTC + time zone offset (no DST offset) \n
			:return: dst: No help available
		"""
		response = self._core.io.query_str('SYSTem:TIME:DSTime:MODE?')
		return Conversions.str_to_bool(response)

	def set_mode(self, dst: bool) -> None:
		"""SCPI: SYSTem:TIME:DSTime:MODE \n
		Snippet: driver.system.time.daylightSavingTime.set_mode(dst = False) \n
		Configures whether the operating system automatically adjusts its clock for daylight saving time (DST) or not. The rules
		defining when exactly the clock must be adjusted by which offset depend on the configured time zone, see method RsCmwBase.
		System.Time.DaylightSavingTime.Rule.value. If the automatism is disabled, the local time is calculated as: Local time =
		UTC + time zone offset (no DST offset) \n
			:param dst: 1: automatism enabled 0: automatism disabled
		"""
		param = Conversions.bool_to_str(dst)
		self._core.io.write(f'SYSTem:TIME:DSTime:MODE {param}')

	def clone(self) -> 'DaylightSavingTime':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DaylightSavingTime(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
