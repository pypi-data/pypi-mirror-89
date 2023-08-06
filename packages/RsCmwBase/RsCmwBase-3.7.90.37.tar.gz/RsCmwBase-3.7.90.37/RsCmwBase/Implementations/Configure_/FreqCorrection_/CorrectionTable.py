from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CorrectionTable:
	"""CorrectionTable commands group definition. 10 total commands, 9 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("correctionTable", core, parent)

	@property
	def create(self):
		"""create commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_create'):
			from .CorrectionTable_.Create import Create
			self._create = Create(self._core, self._base)
		return self._create

	@property
	def erase(self):
		"""erase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_erase'):
			from .CorrectionTable_.Erase import Erase
			self._erase = Erase(self._core, self._base)
		return self._erase

	@property
	def add(self):
		"""add commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_add'):
			from .CorrectionTable_.Add import Add
			self._add = Add(self._core, self._base)
		return self._add

	@property
	def deleteAll(self):
		"""deleteAll commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_deleteAll'):
			from .CorrectionTable_.DeleteAll import DeleteAll
			self._deleteAll = DeleteAll(self._core, self._base)
		return self._deleteAll

	@property
	def length(self):
		"""length commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_length'):
			from .CorrectionTable_.Length import Length
			self._length = Length(self._core, self._base)
		return self._length

	@property
	def details(self):
		"""details commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_details'):
			from .CorrectionTable_.Details import Details
			self._details = Details(self._core, self._base)
		return self._details

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .CorrectionTable_.Catalog import Catalog
			self._catalog = Catalog(self._core, self._base)
		return self._catalog

	@property
	def count(self):
		"""count commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_count'):
			from .CorrectionTable_.Count import Count
			self._count = Count(self._core, self._base)
		return self._count

	@property
	def exist(self):
		"""exist commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_exist'):
			from .CorrectionTable_.Exist import Exist
			self._exist = Exist(self._core, self._base)
		return self._exist

	def delete(self, table_name: str) -> None:
		"""SCPI: CONFigure:BASE:FDCorrection:CTABle:DELete \n
		Snippet: driver.configure.freqCorrection.correctionTable.delete(table_name = '1') \n
		Deletes a correction table from the RAM and the system drive. \n
			:param table_name: String parameter identifying the table. To display a list of existing tables, use the command CONFigure:BASE:FDCorrection:CTABle:CATalog?. You can add the prefix 'instn/' to address subinstrument number n+1.
		"""
		param = Conversions.value_to_quoted_str(table_name)
		self._core.io.write(f'CONFigure:BASE:FDCorrection:CTABle:DELete {param}')

	def clone(self) -> 'CorrectionTable':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CorrectionTable(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
