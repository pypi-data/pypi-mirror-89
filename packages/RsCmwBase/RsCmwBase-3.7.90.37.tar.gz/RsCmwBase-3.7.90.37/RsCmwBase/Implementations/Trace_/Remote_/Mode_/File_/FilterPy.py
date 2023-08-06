from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPy:
	"""FilterPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("filterPy", core, parent)

	# noinspection PyTypeChecker
	class FilterPyStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Binput: bool: No parameter help available
			- Boutput: bool: No parameter help available
			- Berror: bool: No parameter help available
			- Btrigger: bool: No parameter help available
			- Bdevice_Clear: bool: No parameter help available
			- Bstatus_Register: bool: No parameter help available
			- Bconnection: bool: No parameter help available
			- Bremote_Local_Events: bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Binput'),
			ArgStruct.scalar_bool('Boutput'),
			ArgStruct.scalar_bool('Berror'),
			ArgStruct.scalar_bool('Btrigger'),
			ArgStruct.scalar_bool('Bdevice_Clear'),
			ArgStruct.scalar_bool('Bstatus_Register'),
			ArgStruct.scalar_bool('Bconnection'),
			ArgStruct.scalar_bool('Bremote_Local_Events')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Binput: bool = None
			self.Boutput: bool = None
			self.Berror: bool = None
			self.Btrigger: bool = None
			self.Bdevice_Clear: bool = None
			self.Bstatus_Register: bool = None
			self.Bconnection: bool = None
			self.Bremote_Local_Events: bool = None

	def set(self, structure: FilterPyStruct, fileNr=repcap.FileNr.Default) -> None:
		"""SCPI: TRACe:REMote:MODE:FILE<instrument>:FILTer \n
		Snippet: driver.trace.remote.mode.file.filterPy.set(value = [PROPERTY_STRUCT_NAME](), fileNr = repcap.FileNr.Default) \n
		Specifies a filter for tracing of the specified subinstrument. The filter defines which message types and events are
		traced into a file. The default setting is ON,ON,ON,OFF,OFF,OFF,OFF,OFF. All parameters support ON | OFF | 1 | 0. \n
			:param structure: for set value, see the help for FilterPyStruct structure arguments.
			:param fileNr: optional repeated capability selector. Default value: Nr1 (settable in the interface 'File')"""
		fileNr_cmd_val = self._base.get_repcap_cmd_value(fileNr, repcap.FileNr)
		self._core.io.write_struct(f'TRACe:REMote:MODE:FILE{fileNr_cmd_val}:FILTer', structure)

	def get(self, fileNr=repcap.FileNr.Default) -> FilterPyStruct:
		"""SCPI: TRACe:REMote:MODE:FILE<instrument>:FILTer \n
		Snippet: value: FilterPyStruct = driver.trace.remote.mode.file.filterPy.get(fileNr = repcap.FileNr.Default) \n
		Specifies a filter for tracing of the specified subinstrument. The filter defines which message types and events are
		traced into a file. The default setting is ON,ON,ON,OFF,OFF,OFF,OFF,OFF. All parameters support ON | OFF | 1 | 0. \n
			:param fileNr: optional repeated capability selector. Default value: Nr1 (settable in the interface 'File')
			:return: structure: for return value, see the help for FilterPyStruct structure arguments."""
		fileNr_cmd_val = self._base.get_repcap_cmd_value(fileNr, repcap.FileNr)
		return self._core.io.query_struct(f'TRACe:REMote:MODE:FILE{fileNr_cmd_val}:FILTer?', self.__class__.FilterPyStruct())
