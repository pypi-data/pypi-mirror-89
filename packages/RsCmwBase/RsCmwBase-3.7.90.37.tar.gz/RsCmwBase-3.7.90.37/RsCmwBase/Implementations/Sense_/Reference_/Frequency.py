from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def get_locked(self) -> bool:
		"""SCPI: SENSe:BASE:REFerence:FREQuency:LOCKed \n
		Snippet: value: bool = driver.sense.reference.frequency.get_locked() \n
		Queries whether the reference frequency is locked or not. \n
			:return: lock: 1 | 0 1: The frequency is locked. 0: The frequency is not locked.
		"""
		response = self._core.io.query_str('SENSe:BASE:REFerence:FREQuency:LOCKed?')
		return Conversions.str_to_bool(response)
