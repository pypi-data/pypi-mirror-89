from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.Utilities import trim_str_response
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Description:
	"""Description commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("description", core, parent)

	def get(self, producttype: enums.ProductType = None, validity: enums.ValidityScope = None, scope: enums.ValidityScopeB = None, instrumentno: float = None) -> str:
		"""SCPI: SYSTem:BASE:OPTion:DESCription \n
		Snippet: value: str = driver.system.option.description.get(producttype = enums.ProductType.ALL, validity = enums.ValidityScope.ALL, scope = enums.ValidityScopeB.INSTrument, instrumentno = 1.0) \n
		No command help available \n
			:param producttype: No help available
			:param validity: No help available
			:param scope: No help available
			:param instrumentno: No help available
			:return: optionlist: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('producttype', producttype, DataType.Enum, True), ArgSingle('validity', validity, DataType.Enum, True), ArgSingle('scope', scope, DataType.Enum, True), ArgSingle('instrumentno', instrumentno, DataType.Float, True))
		response = self._core.io.query_str(f'SYSTem:BASE:OPTion:DESCription? {param}'.rstrip())
		return trim_str_response(response)
