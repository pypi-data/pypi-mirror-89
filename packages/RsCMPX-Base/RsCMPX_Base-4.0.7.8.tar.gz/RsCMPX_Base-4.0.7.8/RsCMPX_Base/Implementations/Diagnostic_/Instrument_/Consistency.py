from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Consistency:
	"""Consistency commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("consistency", core, parent)

	def get(self, appl_name: str) -> int:
		"""SCPI: DIAGnostic:INSTrument:CONSistency \n
		Snippet: value: int = driver.diagnostic.instrument.consistency.get(appl_name = '1') \n
		No command help available \n
			:param appl_name: No help available
			:return: consistent: No help available"""
		param = Conversions.value_to_quoted_str(appl_name)
		response = self._core.io.query_str(f'DIAGnostic:INSTrument:CONSistency? {param}')
		return Conversions.str_to_int(response)
