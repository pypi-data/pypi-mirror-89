from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Erase:
	"""Erase commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("erase", core, parent)

	def set(self, table_name: str, frequency: List[float] = None) -> None:
		"""SCPI: CONFigure:BASE:FDCorrection:CTABle:ERASe \n
		Snippet: driver.configure.freqCorrection.correctionTable.erase.set(table_name = '1', frequency = [1.1, 2.2, 3.3]) \n
		Removes one or more selected entries from a correction table. Each table entry consists of a frequency value and a
		correction value. Entries to be removed are selected via their frequency values. The supported frequency range depends on
		the instrument model and the available options. The supported range can be smaller than stated here. See 'R&S CMW Models'. \n
			:param table_name: String parameter identifying the table. To display a list of existing tables, use the command CONFigure:BASE:FDCorrection:CTABle:CATalog?. You can add the prefix 'instn/' to address subinstrument number n+1.
			:param frequency: Selects the table entry to be removed. The value must match the frequency of an existing table entry. To remove several entries, specify a comma-separated list of frequencies. Range: 70 MHz to 6 GHz, Unit: Hz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('table_name', table_name, DataType.String), ArgSingle('frequency', frequency, DataType.FloatList, True, True, 1))
		self._core.io.write(f'CONFigure:BASE:FDCorrection:CTABle:ERASe {param}'.rstrip())
