from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Length:
	"""Length commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("length", core, parent)

	def get(self, table_name: str) -> int:
		"""SCPI: CONFigure:BASE:FDCorrection:CTABle:LENGth \n
		Snippet: value: int = driver.configure.freqCorrection.correctionTable.length.get(table_name = '1') \n
		Returns the number of entries (i.e. pairs of frequency and attenuation) of a correction table. \n
			:param table_name: String parameter identifying the table. To display a list of existing tables, use the command method RsCmwBase.Configure.FreqCorrection.CorrectionTable.Catalog.get_. You can add the prefix 'instn/' to address subinstrument number n+1.
			:return: table_length: Number of table entries"""
		param = Conversions.value_to_quoted_str(table_name)
		response = self._core.io.query_str(f'CONFigure:BASE:FDCorrection:CTABle:LENGth? {param}')
		return Conversions.str_to_int(response)
