from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Item:
	"""Item commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("item", core, parent)

	def set(self, item_name: str, file_name: str) -> None:
		"""SCPI: MMEMory:STORe:ITEM \n
		Snippet: driver.massMemory.store.item.set(item_name = '1', file_name = '1') \n
		Executes a partial save, i.e. stores a part of the instrument settings to the specified file. You can store all settings
		of a specific application instance, for example of the LTE signaling application instance 1. Or you can store the list
		mode settings of a specific measurement application instance, for example the list mode settings of the LTE
		multi-evaluation measurement instance 1. \n
			:param item_name: String parameter identifying the part to be saved. ItemName = Application[i][:MEV:LIST] For Application, see method RsCmwBase.MassMemory.Load.Item.set. i is the instance of the application. Omitting i stores instance 1. Appending :MEV:LIST stores only the list mode settings.
			:param file_name: String parameter specifying the path and filename of the target file. Wildcards are not allowed.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('item_name', item_name, DataType.String), ArgSingle('file_name', file_name, DataType.String))
		self._core.io.write(f'MMEMory:STORe:ITEM {param}'.rstrip())
