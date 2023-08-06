from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def set(self, path: str, reserve: str) -> None:
		"""SCPI: WRITe:EEPRom:DATA \n
		Snippet: driver.write.eeprom.data.set(path = '1', reserve = '1') \n
		No command help available \n
			:param path: No help available
			:param reserve: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('path', path, DataType.String), ArgSingle('reserve', reserve, DataType.String))
		self._core.io.write(f'WRITe:EEPRom:DATA {param}'.rstrip())
