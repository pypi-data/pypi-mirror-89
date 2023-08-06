from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Add:
	"""Add commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("add", core, parent)

	def set(self, table_name: str, frequency: List[float] = None, correction: List[float] = None) -> None:
		"""SCPI: CONFigure:BASE:FDCorrection:CTABle:ADD \n
		Snippet: driver.configure.freqCorrection.correctionTable.add.set(table_name = '1', frequency = [1.1, 2.2, 3.3], correction = [1.1, 2.2, 3.3]) \n
		Adds entries to an existing correction table. At least one parameter pair has to be specified. A command with an
		incomplete pair (e.g. <Frequency> without <Correction>) is ignored completely. You can add parameter pairs in any order.
		The table entries (pairs) are automatically sorted from lowest to highest frequency. The supported frequency range
		depends on the instrument model and the available options. The supported range can be smaller than stated here. See 'R&S
		CMW Models'. \n
			:param table_name: String parameter identifying the table. To display a list of existing tables, use the command CONFigure:BASE:FDCorrection:CTABle:CATalog?. You can add the prefix 'instn/' to address subinstrument number n+1.
			:param frequency: Range: 70 MHz to 6 GHz, Unit: Hz
			:param correction: Range: -50 dB to 90 dB, Unit: dB
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('table_name', table_name, DataType.String), ArgSingle('frequency', frequency, DataType.FloatList, True, True, 1), ArgSingle('correction', correction, DataType.FloatList, True, True, 1))
		self._core.io.write(f'CONFigure:BASE:FDCorrection:CTABle:ADD {param}'.rstrip())
