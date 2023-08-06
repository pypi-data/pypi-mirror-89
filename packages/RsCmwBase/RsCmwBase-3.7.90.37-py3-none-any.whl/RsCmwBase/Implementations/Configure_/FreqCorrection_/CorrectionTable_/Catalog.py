from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Catalog:
	"""Catalog commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("catalog", core, parent)

	def get(self, table_path: str = None) -> List[str]:
		"""SCPI: CONFigure:BASE:FDCorrection:CTABle:CATalog \n
		Snippet: value: List[str] = driver.configure.freqCorrection.correctionTable.catalog.get(table_path = '1') \n
		Returns the names of the correction tables currently stored on the system drive for a selected subinstrument. \n
			:param table_path: String selecting the subinstrument If omitted: subinstrument addressed by the remote channel. 'instn': subinstrument n+1
			:return: tablename: Comma-separated list of table names as strings"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('table_path', table_path, DataType.String, True))
		response = self._core.io.query_str(f'CONFigure:BASE:FDCorrection:CTABle:CATalog? {param}'.rstrip())
		return Conversions.str_to_str_list(response)
