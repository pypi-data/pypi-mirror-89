from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Utilities import trim_str_response
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vresource:
	"""Vresource commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("vresource", core, parent)

	def get(self, hislipInstance=repcap.HislipInstance.Default) -> str:
		"""SCPI: SYSTem:COMMunicate:HISLip<inst>:VRESource \n
		Snippet: value: str = driver.system.communicate.hislip.vresource.get(hislipInstance = repcap.HislipInstance.Default) \n
		Queries the VISA resource string for the HiSLIP protocol. \n
			:param hislipInstance: optional repeated capability selector. Default value: Inst1 (settable in the interface 'Hislip')
			:return: visaresource: No help available"""
		hislipInstance_cmd_val = self._base.get_repcap_cmd_value(hislipInstance, repcap.HislipInstance)
		response = self._core.io.query_str(f'SYSTem:COMMunicate:HISLip{hislipInstance_cmd_val}:VRESource?')
		return trim_str_response(response)
