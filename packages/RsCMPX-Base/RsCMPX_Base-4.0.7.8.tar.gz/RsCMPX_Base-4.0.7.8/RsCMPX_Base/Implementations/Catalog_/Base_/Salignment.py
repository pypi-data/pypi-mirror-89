from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Salignment:
	"""Salignment commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("salignment", core, parent)

	def get_slot(self) -> str:
		"""SCPI: CATalog:BASE:SALignment:SLOT \n
		Snippet: value: str = driver.catalog.base.salignment.get_slot() \n
		No command help available \n
			:return: slotlist: No help available
		"""
		response = self._core.io.query_str('CATalog:BASE:SALignment:SLOT?')
		return trim_str_response(response)
