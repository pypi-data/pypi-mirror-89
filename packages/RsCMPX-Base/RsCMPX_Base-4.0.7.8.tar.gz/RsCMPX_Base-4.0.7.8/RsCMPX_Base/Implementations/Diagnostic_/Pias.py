from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pias:
	"""Pias commands group definition. 5 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pias", core, parent)

	@property
	def scan(self):
		"""scan commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scan'):
			from .Pias_.Scan import Scan
			self._scan = Scan(self._core, self._base)
		return self._scan

	@property
	def connect(self):
		"""connect commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_connect'):
			from .Pias_.Connect import Connect
			self._connect = Connect(self._core, self._base)
		return self._connect

	def get_host(self) -> str:
		"""SCPI: DIAGnostic:PIAS:HOST \n
		Snippet: value: str = driver.diagnostic.pias.get_host() \n
		No command help available \n
			:return: hostname: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:PIAS:HOST?')
		return trim_str_response(response)

	def get_id(self) -> str:
		"""SCPI: DIAGnostic:PIAS:ID \n
		Snippet: value: str = driver.diagnostic.pias.get_id() \n
		No command help available \n
			:return: pias_id: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:PIAS:ID?')
		return trim_str_response(response)

	def clone(self) -> 'Pias':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pias(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
