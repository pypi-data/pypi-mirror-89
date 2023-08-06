from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TxFilter:
	"""TxFilter commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: TxFilter, default value after init: TxFilter.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("txFilter", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_txFilter_get', 'repcap_txFilter_set', repcap.TxFilter.Nr1)

	def repcap_txFilter_set(self, enum_value: repcap.TxFilter) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TxFilter.Default
		Default value after init: TxFilter.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_txFilter_get(self) -> repcap.TxFilter:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def fetch(self, slot=repcap.Slot.Default, txFilter=repcap.TxFilter.Default) -> List[float]:
		"""SCPI: FETCh:BASE:CORRection:IFEQualizer:TRACe:MAGNitude:UNCorrected:SLOT<Slot>:TXFilter<Filter> \n
		Snippet: value: List[float] = driver.correction.ifEqualizer.trace.magnitude.uncorrected.slot.txFilter.fetch(slot = repcap.Slot.Default, txFilter = repcap.TxFilter.Default) \n
		No command help available \n
		Use RsCmwBase.reliability.last_value to read the updated reliability indicator. \n
			:param slot: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param txFilter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'TxFilter')
			:return: value: No help available"""
		slot_cmd_val = self._base.get_repcap_cmd_value(slot, repcap.Slot)
		txFilter_cmd_val = self._base.get_repcap_cmd_value(txFilter, repcap.TxFilter)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:BASE:CORRection:IFEQualizer:TRACe:MAGNitude:UNCorrected:SLOT{slot_cmd_val}:TXFilter{txFilter_cmd_val}?', suppressed)
		return response

	def clone(self) -> 'TxFilter':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TxFilter(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
