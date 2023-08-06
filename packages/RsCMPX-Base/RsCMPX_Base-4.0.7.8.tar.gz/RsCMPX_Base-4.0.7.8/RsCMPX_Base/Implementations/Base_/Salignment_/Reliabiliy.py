from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Reliabiliy:
	"""Reliabiliy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("reliabiliy", core, parent)

	def fetch(self) -> int:
		"""SCPI: FETCh:BASE:SALignment:RELiabiliy \n
		Snippet: value: int = driver.base.salignment.reliabiliy.fetch() \n
		No command help available \n
			:return: reliability: No help available"""
		response = self._core.io.query_str(f'FETCh:BASE:SALignment:RELiabiliy?')
		return Conversions.str_to_int(response)
