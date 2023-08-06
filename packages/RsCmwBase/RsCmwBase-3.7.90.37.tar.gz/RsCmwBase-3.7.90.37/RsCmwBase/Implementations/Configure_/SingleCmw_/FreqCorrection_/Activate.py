from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Activate:
	"""Activate commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("activate", core, parent)

	# noinspection PyTypeChecker
	class RxStruct(StructBase):
		"""Structure for setting input parameters. Contains optional set arguments. Fields: \n
			- Connectorbench: str: Selects a single connector or a connector bench with 4 or 8 connectors For possible values, see 'Values for RF Path Selection'.
			- Table_1: str: String parameter identifying the table for the selected single connector or for the first connector of the selected bench (e.g. 1.1)
			- Table_2: str: Optional setting parameter. String parameter identifying the table for the second connector of the selected bench (e.g. 1.2)
			- Table_3: str: Optional setting parameter. Table for third connector of selected bench (e.g. 1.3)
			- Table_4: str: Optional setting parameter. Table for fourth connector of selected bench (e.g. 1.4)
			- Table_5: str: Optional setting parameter. Table for fifth connector of selected bench (e.g. 1.5)
			- Table_6: str: Optional setting parameter. Table for sixth connector of selected bench (e.g. 1.6)
			- Table_7: str: Optional setting parameter. Table for seventh connector of selected bench (e.g. 1.7)
			- Table_8: str: Optional setting parameter. Table for eighth connector of selected bench (e.g. 1.8)"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Connectorbench'),
			ArgStruct.scalar_str('Table_1'),
			ArgStruct.scalar_str_optional('Table_2'),
			ArgStruct.scalar_str_optional('Table_3'),
			ArgStruct.scalar_str_optional('Table_4'),
			ArgStruct.scalar_str_optional('Table_5'),
			ArgStruct.scalar_str_optional('Table_6'),
			ArgStruct.scalar_str_optional('Table_7'),
			ArgStruct.scalar_str_optional('Table_8')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Connectorbench: str = None
			self.Table_1: str = None
			self.Table_2: str = None
			self.Table_3: str = None
			self.Table_4: str = None
			self.Table_5: str = None
			self.Table_6: str = None
			self.Table_7: str = None
			self.Table_8: str = None

	def set_rx(self, value: RxStruct) -> None:
		"""SCPI: CONFigure:CMWS:FDCorrection:ACTivate:RX \n
		Snippet: driver.configure.singleCmw.freqCorrection.activate.set_rx(value = RxStruct()) \n
		Activates correction tables for R&S CMWS input paths (RX) or output paths (TX) .
			INTRO_CMD_HELP: You can use the commands in two ways: \n
			- To activate a correction table for a selected RF connector of the R&S CMWS, specify a single connector and a single table name.
			- To activate individual correction tables for all RF connectors of a connector bench, select a bench and specify a table for each connector (4 or 8 connectors/tables) .
		You can add the prefix 'inst<n>/' to table names to address subinstrument number <n>+1. \n
			:param value: see the help for RxStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:CMWS:FDCorrection:ACTivate:RX', value)

	# noinspection PyTypeChecker
	class TxStruct(StructBase):
		"""Structure for setting input parameters. Contains optional set arguments. Fields: \n
			- Connectorbench: str: Selects a single connector or a connector bench with 4 or 8 connectors For possible values, see 'Values for RF Path Selection'.
			- Table_1: str: String parameter identifying the table for the selected single connector or for the first connector of the selected bench (e.g. 1.1)
			- Table_2: str: Optional setting parameter. String parameter identifying the table for the second connector of the selected bench (e.g. 1.2)
			- Table_3: str: Optional setting parameter. Table for third connector of selected bench (e.g. 1.3)
			- Table_4: str: Optional setting parameter. Table for fourth connector of selected bench (e.g. 1.4)
			- Table_5: str: Optional setting parameter. Table for fifth connector of selected bench (e.g. 1.5)
			- Table_6: str: Optional setting parameter. Table for sixth connector of selected bench (e.g. 1.6)
			- Table_7: str: Optional setting parameter. Table for seventh connector of selected bench (e.g. 1.7)
			- Table_8: str: Optional setting parameter. Table for eighth connector of selected bench (e.g. 1.8)"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Connectorbench'),
			ArgStruct.scalar_str('Table_1'),
			ArgStruct.scalar_str_optional('Table_2'),
			ArgStruct.scalar_str_optional('Table_3'),
			ArgStruct.scalar_str_optional('Table_4'),
			ArgStruct.scalar_str_optional('Table_5'),
			ArgStruct.scalar_str_optional('Table_6'),
			ArgStruct.scalar_str_optional('Table_7'),
			ArgStruct.scalar_str_optional('Table_8')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Connectorbench: str = None
			self.Table_1: str = None
			self.Table_2: str = None
			self.Table_3: str = None
			self.Table_4: str = None
			self.Table_5: str = None
			self.Table_6: str = None
			self.Table_7: str = None
			self.Table_8: str = None

	def set_tx(self, value: TxStruct) -> None:
		"""SCPI: CONFigure:CMWS:FDCorrection:ACTivate:TX \n
		Snippet: driver.configure.singleCmw.freqCorrection.activate.set_tx(value = TxStruct()) \n
		Activates correction tables for R&S CMWS input paths (RX) or output paths (TX) .
			INTRO_CMD_HELP: You can use the commands in two ways: \n
			- To activate a correction table for a selected RF connector of the R&S CMWS, specify a single connector and a single table name.
			- To activate individual correction tables for all RF connectors of a connector bench, select a bench and specify a table for each connector (4 or 8 connectors/tables) .
		You can add the prefix 'inst<n>/' to table names to address subinstrument number <n>+1. \n
			:param value: see the help for TxStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:CMWS:FDCorrection:ACTivate:TX', value)
