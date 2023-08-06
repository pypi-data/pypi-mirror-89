from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Queue:
	"""Queue commands group definition. 3 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("queue", core, parent)

	@property
	def push(self):
		"""push commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_push'):
			from .Queue_.Push import Push
			self._push = Push(self._core, self._base)
		return self._push

	def get_size(self) -> int:
		"""SCPI: DIAGnostic:ERRor:QUEue:SIZE \n
		Snippet: value: int = driver.diagnostic.error.queue.get_size() \n
		No command help available \n
			:return: size: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:ERRor:QUEue:SIZE?')
		return Conversions.str_to_int(response)

	def set_size(self, size: int) -> None:
		"""SCPI: DIAGnostic:ERRor:QUEue:SIZE \n
		Snippet: driver.diagnostic.error.queue.set_size(size = 1) \n
		No command help available \n
			:param size: No help available
		"""
		param = Conversions.decimal_value_to_str(size)
		self._core.io.write(f'DIAGnostic:ERRor:QUEue:SIZE {param}')

	def get_length(self) -> int:
		"""SCPI: DIAGnostic:ERRor:QUEue:LENGth \n
		Snippet: value: int = driver.diagnostic.error.queue.get_length() \n
		No command help available \n
			:return: text_length: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:ERRor:QUEue:LENGth?')
		return Conversions.str_to_int(response)

	def set_length(self, text_length: int) -> None:
		"""SCPI: DIAGnostic:ERRor:QUEue:LENGth \n
		Snippet: driver.diagnostic.error.queue.set_length(text_length = 1) \n
		No command help available \n
			:param text_length: No help available
		"""
		param = Conversions.decimal_value_to_str(text_length)
		self._core.io.write(f'DIAGnostic:ERRor:QUEue:LENGth {param}')

	def clone(self) -> 'Queue':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Queue(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
