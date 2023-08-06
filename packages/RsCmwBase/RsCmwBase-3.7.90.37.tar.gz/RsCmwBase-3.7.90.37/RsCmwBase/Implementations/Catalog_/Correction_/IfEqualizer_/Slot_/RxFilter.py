from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RxFilter:
	"""RxFilter commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rxFilter", core, parent)

	def get(self, slot=repcap.Slot.Default) -> List[str]:
		"""SCPI: CATalog:BASE:CORRection:IFEQualizer:SLOT<Slot>:RXFilter \n
		Snippet: value: List[str] = driver.catalog.correction.ifEqualizer.slot.rxFilter.get(slot = repcap.Slot.Default) \n
		No command help available \n
			:param slot: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:return: filter_py: No help available"""
		slot_cmd_val = self._base.get_repcap_cmd_value(slot, repcap.Slot)
		response = self._core.io.query_str(f'CATalog:BASE:CORRection:IFEQualizer:SLOT{slot_cmd_val}:RXFilter?')
		return Conversions.str_to_str_list(response)
