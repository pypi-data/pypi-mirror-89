from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class All:
	"""All commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("all", core, parent)

	def set(self, table_path: str = None) -> None:
		"""SCPI: CONFigure:CMWS:FDCorrection:DEACtivate:RX:ALL \n
		Snippet: driver.configure.singleCmw.freqCorrection.deactivate.rx.all.set(table_path = '1') \n
		Deactivate all correction tables for all R&S CMWS RF connectors of a selected subinstrument, in input direction (RX) or
		output direction (TX) . \n
			:param table_path: String selecting the subinstrument If omitted: subinstrument addressed by the remote channel. 'instn': subinstrument n+1
		"""
		param = ''
		if table_path:
			param = Conversions.value_to_quoted_str(table_path)
		self._core.io.write(f'CONFigure:CMWS:FDCorrection:DEACtivate:RX:ALL {param}'.strip())
