from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- State: enums.MutexState: No parameter help available
			- Key: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_enum('State', enums.MutexState),
			ArgStruct.scalar_int('Key')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.State: enums.MutexState = None
			self.Key: int = None

	def get(self, name: str, action: enums.MutexAction = None, timeout: float = None) -> GetStruct:
		"""SCPI: CONFigure:MUTex:STATe \n
		Snippet: value: GetStruct = driver.configure.mutex.state.get(name = '1', action = enums.MutexAction.DONothing, timeout = 1.0) \n
		No command help available \n
			:param name: No help available
			:param action: No help available
			:param timeout: No help available
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('name', name, DataType.String), ArgSingle('action', action, DataType.Enum, True), ArgSingle('timeout', timeout, DataType.Float, True))
		return self._core.io.query_struct(f'CONFigure:MUTex:STATe? {param}'.rstrip(), self.__class__.GetStruct())
