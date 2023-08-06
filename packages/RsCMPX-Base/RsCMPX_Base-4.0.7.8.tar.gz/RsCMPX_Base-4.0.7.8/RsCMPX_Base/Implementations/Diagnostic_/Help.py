from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Help:
	"""Help commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("help", core, parent)

	@property
	def syntax(self):
		"""syntax commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_syntax'):
			from .Help_.Syntax import Syntax
			self._syntax = Syntax(self._core, self._base)
		return self._syntax

	def get_headers(self) -> bytes:
		"""SCPI: DIAGnostic:HELP:HEADers \n
		Snippet: value: bytes = driver.diagnostic.help.get_headers() \n
		No command help available \n
			:return: header: No help available
		"""
		response = self._core.io.query_bin_block('DIAGnostic:HELP:HEADers?')
		return response

	def clone(self) -> 'Help':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Help(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
