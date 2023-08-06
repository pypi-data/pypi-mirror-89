from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.Utilities import trim_str_response
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ListPy:
	"""ListPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("listPy", core, parent)

	def get(self, producttype: enums.ProductType = None, validity: enums.ValidityScope = None, scope: enums.ValidityScopeB = None, instrumentno: float = None) -> str:
		"""SCPI: SYSTem:BASE:OPTion:LIST \n
		Snippet: value: str = driver.system.base.option.listPy.get(producttype = enums.ProductType.ALL, validity = enums.ValidityScope.ALL, scope = enums.ValidityScopeB.INSTrument, instrumentno = 1.0) \n
		Returns a list of installed software options (licenses) , hardware options, software packages and firmware applications.
		The list can be filtered using the described parameters. If filtering results in an empty list, a '0' is returned.
			INTRO_CMD_HELP: The meaning of the filter <Validity> depends on the <OptionType> as follows: \n
			- A software option is valid if there is an active license key for it. The value 'FUNCtional' is not relevant.
			- A hardware option is functional if the corresponding hardware and all its components can be used (no defect detected) . The value 'VALid' is not relevant.
			- A firmware application is functional if the required hardware, software and license keys are available and functional. The value 'VALid' is not relevant.
			- For software packages, the filter has no effect.  \n
			:param producttype: No help available
			:param validity: List only functional entries or only valid entries. By default or if ALL is selected, the list is not filtered according to the validity.
			:param scope: No help available
			:param instrumentno: No help available
			:return: optionlist: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('producttype', producttype, DataType.Enum, True), ArgSingle('validity', validity, DataType.Enum, True), ArgSingle('scope', scope, DataType.Enum, True), ArgSingle('instrumentno', instrumentno, DataType.Float, True))
		response = self._core.io.query_str(f'SYSTem:BASE:OPTion:LIST? {param}'.rstrip())
		return trim_str_response(response)
