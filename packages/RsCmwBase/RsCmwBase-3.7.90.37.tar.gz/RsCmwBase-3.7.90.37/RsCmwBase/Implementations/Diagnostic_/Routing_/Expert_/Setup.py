from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setup:
	"""Setup commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("setup", core, parent)

	def set(self, routingname: str, data: List[enums.ExpertSetup]) -> None:
		"""SCPI: DIAGnostic:ROUTing:EXPert:SETup \n
		Snippet: driver.diagnostic.routing.expert.setup.set(routingname = '1', data = [ExpertSetup.BBG1, ExpertSetup.SUW7]) \n
		No command help available \n
			:param routingname: No help available
			:param data: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('routingname', routingname, DataType.String), ArgSingle.as_open_list('data', data, DataType.EnumList))
		self._core.io.write(f'DIAGnostic:ROUTing:EXPert:SETup {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self, routingname: str) -> List[enums.ExpertSetup]:
		"""SCPI: DIAGnostic:ROUTing:EXPert:SETup \n
		Snippet: value: List[enums.ExpertSetup] = driver.diagnostic.routing.expert.setup.get(routingname = '1') \n
		No command help available \n
			:param routingname: No help available
			:return: data: No help available"""
		param = Conversions.value_to_quoted_str(routingname)
		response = self._core.io.query_str(f'DIAGnostic:ROUTing:EXPert:SETup? {param}')
		return Conversions.str_to_list_enum(response, enums.ExpertSetup)
