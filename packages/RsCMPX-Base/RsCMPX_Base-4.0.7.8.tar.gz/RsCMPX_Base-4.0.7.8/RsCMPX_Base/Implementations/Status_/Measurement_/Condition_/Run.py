from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.Utilities import trim_str_response
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Run:
	"""Run commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("run", core, parent)

	def get(self, filter_py: str = None, mode: enums.ExpressionMode = None) -> str:
		"""SCPI: STATus:MEASurement:CONDition:RUN \n
		Snippet: value: str = driver.status.measurement.condition.run.get(filter_py = '1', mode = enums.ExpressionMode.REGex) \n
		No command help available \n
			:param filter_py: No help available
			:param mode: No help available
			:return: bitname: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('filter_py', filter_py, DataType.String, True), ArgSingle('mode', mode, DataType.Enum, True))
		response = self._core.io.query_str(f'STATus:MEASurement:CONDition:RUN? {param}'.rstrip())
		return trim_str_response(response)
