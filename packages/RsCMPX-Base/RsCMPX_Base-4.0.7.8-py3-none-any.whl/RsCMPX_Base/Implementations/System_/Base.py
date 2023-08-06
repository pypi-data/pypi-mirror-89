from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Base:
	"""Base commands group definition. 30 total commands, 8 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("base", core, parent)

	@property
	def ipSubnet(self):
		"""ipSubnet commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ipSubnet'):
			from .Base_.IpSubnet import IpSubnet
			self._ipSubnet = IpSubnet(self._core, self._base)
		return self._ipSubnet

	@property
	def device(self):
		"""device commands group. 0 Sub-classes, 7 commands."""
		if not hasattr(self, '_device'):
			from .Base_.Device import Device
			self._device = Device(self._core, self._base)
		return self._device

	@property
	def reference(self):
		"""reference commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_reference'):
			from .Base_.Reference import Reference
			self._reference = Reference(self._core, self._base)
		return self._reference

	@property
	def ssync(self):
		"""ssync commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ssync'):
			from .Base_.Ssync import Ssync
			self._ssync = Ssync(self._core, self._base)
		return self._ssync

	@property
	def option(self):
		"""option commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_option'):
			from .Base_.Option import Option
			self._option = Option(self._core, self._base)
		return self._option

	@property
	def password(self):
		"""password commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_password'):
			from .Base_.Password import Password
			self._password = Password(self._core, self._base)
		return self._password

	@property
	def display(self):
		"""display commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_display'):
			from .Base_.Display import Display
			self._display = Display(self._core, self._base)
		return self._display

	@property
	def stIcon(self):
		"""stIcon commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_stIcon'):
			from .Base_.StIcon import StIcon
			self._stIcon = StIcon(self._core, self._base)
		return self._stIcon

	def get_reliability(self) -> int:
		"""SCPI: SYSTem:BASE:RELiability \n
		Snippet: value: int = driver.system.base.get_reliability() \n
		Returns a reliability value indicating errors detected by the base software. \n
			:return: value: For reliability indicator values, see 'Checking the Reliability Indicator'
		"""
		response = self._core.io.query_str('SYSTem:BASE:RELiability?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'Base':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Base(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
