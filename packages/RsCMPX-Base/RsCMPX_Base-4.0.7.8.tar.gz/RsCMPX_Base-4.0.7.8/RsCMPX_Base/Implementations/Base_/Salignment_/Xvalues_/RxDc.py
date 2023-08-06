from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RxDc:
	"""RxDc commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rxDc", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:BASE:SALignment:XVALues:RXDC \n
		Snippet: value: List[float] = driver.base.salignment.xvalues.rxDc.fetch() \n
		No command help available \n
		Suppressed linked return values: reliability \n
			:return: value: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:BASE:SALignment:XVALues:RXDC?', suppressed)
		return response
