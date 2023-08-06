from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Multiple:
	"""Multiple commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("multiple", core, parent)

	def get(self, handle: List[str]) -> int:
		"""SCPI: DIAGnostic:PIAS:CONNect:MULTiple \n
		Snippet: value: int = driver.diagnostic.pias.connect.multiple.get(handle = ['1', '2', '3']) \n
		No command help available \n
			:param handle: No help available
			:return: result: No help available"""
		param = Conversions.list_to_csv_quoted_str(handle)
		response = self._core.io.query_str(f'DIAGnostic:PIAS:CONNect:MULTiple? {param}')
		return Conversions.str_to_int(response)
