from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Display:
	"""Display commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("display", core, parent)

	@property
	def monitor(self):
		"""monitor commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_monitor'):
			from .Display_.Monitor import Monitor
			self._monitor = Monitor(self._core, self._base)
		return self._monitor

	def get_update(self) -> bool:
		"""SCPI: SYSTem:DISPlay:UPDate \n
		Snippet: value: bool = driver.system.display.get_update() \n
		No command help available \n
			:return: displayupdate: No help available
		"""
		response = self._core.io.query_str('SYSTem:DISPlay:UPDate?')
		return Conversions.str_to_bool(response)

	def set_update(self, displayupdate: bool) -> None:
		"""SCPI: SYSTem:DISPlay:UPDate \n
		Snippet: driver.system.display.set_update(displayupdate = False) \n
		No command help available \n
			:param displayupdate: No help available
		"""
		param = Conversions.bool_to_str(displayupdate)
		self._core.io.write(f'SYSTem:DISPlay:UPDate {param}')

	def clone(self) -> 'Display':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Display(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
