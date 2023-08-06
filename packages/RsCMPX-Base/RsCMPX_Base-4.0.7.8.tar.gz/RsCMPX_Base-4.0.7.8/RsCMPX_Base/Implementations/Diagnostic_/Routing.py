from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Routing:
	"""Routing commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("routing", core, parent)

	@property
	def expert(self):
		"""expert commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_expert'):
			from .Routing_.Expert import Expert
			self._expert = Expert(self._core, self._base)
		return self._expert

	def get_catalog(self) -> List[str]:
		"""SCPI: DIAGnostic:ROUTing:CATalog \n
		Snippet: value: List[str] = driver.diagnostic.routing.get_catalog() \n
		No command help available \n
			:return: routing_name: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:ROUTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def clone(self) -> 'Routing':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Routing(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
