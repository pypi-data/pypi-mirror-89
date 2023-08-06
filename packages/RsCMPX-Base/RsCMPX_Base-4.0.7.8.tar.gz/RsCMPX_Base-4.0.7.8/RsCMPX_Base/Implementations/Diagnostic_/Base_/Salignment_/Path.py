from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Path:
	"""Path commands group definition. 6 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("path", core, parent)

	@property
	def iq(self):
		"""iq commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_iq'):
			from .Path_.Iq import Iq
			self._iq = Iq(self._core, self._base)
		return self._iq

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_level'):
			from .Path_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	def clone(self) -> 'Path':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Path(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
