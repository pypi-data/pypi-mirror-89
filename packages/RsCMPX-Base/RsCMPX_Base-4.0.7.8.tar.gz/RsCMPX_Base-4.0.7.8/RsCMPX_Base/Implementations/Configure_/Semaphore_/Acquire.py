from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Acquire:
	"""Acquire commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("acquire", core, parent)

	def get(self, name: str) -> int:
		"""SCPI: CONFigure:SEMaphore:ACQuire \n
		Snippet: value: int = driver.configure.semaphore.acquire.get(name = '1') \n
		No command help available \n
			:param name: No help available
			:return: key: No help available"""
		param = Conversions.value_to_quoted_str(name)
		response = self._core.io.query_str(f'CONFigure:SEMaphore:ACQuire? {param}')
		return Conversions.str_to_int(response)
