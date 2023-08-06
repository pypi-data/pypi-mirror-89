from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Count:
	"""Count commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("count", core, parent)

	def get(self, table_path: str = None) -> int:
		"""SCPI: CONFigure:BASE:FDCorrection:CTABle:COUNt \n
		Snippet: value: int = driver.configure.base.freqCorrection.correctionTable.count.get(table_path = '1') \n
		No command help available \n
			:param table_path: No help available
			:return: tablecount: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('table_path', table_path, DataType.String, True))
		response = self._core.io.query_str(f'CONFigure:BASE:FDCorrection:CTABle:COUNt? {param}'.rstrip())
		return Conversions.str_to_int(response)
