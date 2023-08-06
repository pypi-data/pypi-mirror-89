from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IfEqualizer:
	"""IfEqualizer commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ifEqualizer", core, parent)

	@property
	def slot(self):
		"""slot commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_slot'):
			from .IfEqualizer_.Slot import Slot
			self._slot = Slot(self._core, self._base)
		return self._slot

	def get_sname(self) -> List[str]:
		"""SCPI: CATalog:BASE:CORRection:IFEQualizer:SNAMe \n
		Snippet: value: List[str] = driver.catalog.base.correction.ifEqualizer.get_sname() \n
		No command help available \n
			:return: slot: No help available
		"""
		response = self._core.io.query_str('CATalog:BASE:CORRection:IFEQualizer:SNAMe?')
		return Conversions.str_to_str_list(response)

	def clone(self) -> 'IfEqualizer':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IfEqualizer(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
