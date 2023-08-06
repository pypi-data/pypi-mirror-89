from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserInitiated:
	"""UserInitiated commands group definition. 1 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: Trigger, default value after init: Trigger.Trg1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("userInitiated", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_trigger_get', 'repcap_trigger_set', repcap.Trigger.Trg1)

	def repcap_trigger_set(self, enum_value: repcap.Trigger) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Trigger.Default
		Default value after init: Trigger.Trg1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_trigger_get(self) -> repcap.Trigger:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .UserInitiated_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	def clone(self) -> 'UserInitiated':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UserInitiated(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
