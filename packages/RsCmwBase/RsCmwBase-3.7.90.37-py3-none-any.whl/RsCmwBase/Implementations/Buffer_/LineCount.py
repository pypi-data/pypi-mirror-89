from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LineCount:
	"""LineCount commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lineCount", core, parent)

	def fetch(self, buffer: str) -> int:
		"""SCPI: FETCh:BASE:BUFFer:LINecount \n
		Snippet: value: int = driver.buffer.lineCount.fetch(buffer = '1') \n
		Returns the number of lines in a buffer. \n
			:param buffer: No help available
			:return: size: Number of lines in the buffer."""
		param = Conversions.value_to_quoted_str(buffer)
		response = self._core.io.query_str(f'FETCh:BASE:BUFFer:LINecount? {param}')
		return Conversions.str_to_int(response)
