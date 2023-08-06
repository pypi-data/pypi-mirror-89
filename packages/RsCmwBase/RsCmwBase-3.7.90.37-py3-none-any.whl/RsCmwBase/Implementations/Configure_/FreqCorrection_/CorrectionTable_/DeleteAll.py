from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DeleteAll:
	"""DeleteAll commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("deleteAll", core, parent)

	def set(self, table_path: str = None) -> None:
		"""SCPI: CONFigure:BASE:FDCorrection:CTABle:DELete:ALL \n
		Snippet: driver.configure.freqCorrection.correctionTable.deleteAll.set(table_path = '1') \n
		Deletes all correction tables for a selected subinstrument from the RAM and the system drive. \n
			:param table_path: String selecting the subinstrument If omitted: subinstrument addressed by the remote channel. 'instn': subinstrument n+1
		"""
		param = ''
		if table_path:
			param = Conversions.value_to_quoted_str(table_path)
		self._core.io.write(f'CONFigure:BASE:FDCorrection:CTABle:DELete:ALL {param}'.strip())
