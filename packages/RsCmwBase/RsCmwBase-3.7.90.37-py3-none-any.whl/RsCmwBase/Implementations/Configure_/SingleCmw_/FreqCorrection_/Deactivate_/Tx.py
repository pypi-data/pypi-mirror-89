from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tx:
	"""Tx commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tx", core, parent)

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .Tx_.All import All
			self._all = All(self._core, self._base)
		return self._all

	def set_value(self, connectorbench: str) -> None:
		"""SCPI: CONFigure:CMWS:FDCorrection:DEACtivate:TX \n
		Snippet: driver.configure.singleCmw.freqCorrection.deactivate.tx.set_value(connectorbench = r1) \n
		Deactivate correction tables for a single R&S CMWS RF connector or a connector bench, in input direction (RX) or output
		direction (TX) . \n
			:param connectorbench: Selects a single connector or a connector bench with 4 or 8 connectors For possible values, see 'Values for RF Path Selection'.
		"""
		param = Conversions.value_to_str(connectorbench)
		self._core.io.write(f'CONFigure:CMWS:FDCorrection:DEACtivate:TX {param}')

	def clone(self) -> 'Tx':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tx(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
