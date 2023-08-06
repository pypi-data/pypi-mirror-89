from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IpSubnet:
	"""IpSubnet commands group definition. 7 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ipSubnet", core, parent)

	@property
	def snode(self):
		"""snode commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_snode'):
			from .IpSubnet_.Snode import Snode
			self._snode = Snode(self._core, self._base)
		return self._snode

	@property
	def subMonitor(self):
		"""subMonitor commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_subMonitor'):
			from .IpSubnet_.SubMonitor import SubMonitor
			self._subMonitor = SubMonitor(self._core, self._base)
		return self._subMonitor

	def clone(self) -> 'IpSubnet':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IpSubnet(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
