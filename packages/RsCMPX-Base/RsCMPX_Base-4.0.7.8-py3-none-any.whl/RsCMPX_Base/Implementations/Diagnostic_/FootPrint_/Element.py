from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Element:
	"""Element commands group definition. 5 total commands, 4 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("element", core, parent)

	@property
	def connection(self):
		"""connection commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_connection'):
			from .Element_.Connection import Connection
			self._connection = Connection(self._core, self._base)
		return self._connection

	@property
	def properties(self):
		"""properties commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_properties'):
			from .Element_.Properties import Properties
			self._properties = Properties(self._core, self._base)
		return self._properties

	@property
	def references(self):
		"""references commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_references'):
			from .Element_.References import References
			self._references = References(self._core, self._base)
		return self._references

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Element_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	def get_ids(self) -> List[int]:
		"""SCPI: DIAGnostic:FOOTprint:ELEMent:IDS \n
		Snippet: value: List[int] = driver.diagnostic.footPrint.element.get_ids() \n
		No command help available \n
			:return: element_ids: No help available
		"""
		response = self._core.io.query_bin_or_ascii_int_list('DIAGnostic:FOOTprint:ELEMent:IDS?')
		return response

	def clone(self) -> 'Element':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Element(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
