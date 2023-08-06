from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Types import DataType
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiCmw:
	"""MultiCmw commands group definition. 4 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("multiCmw", core, parent)

	@property
	def identify(self):
		"""identify commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_identify'):
			from .MultiCmw_.Identify import Identify
			self._identify = Identify(self._core, self._base)
		return self._identify

	@property
	def snumber(self):
		"""snumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_snumber'):
			from .MultiCmw_.Snumber import Snumber
			self._snumber = Snumber(self._core, self._base)
		return self._snumber

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .MultiCmw_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def initiate(self, cmw_1: enums.CmwSetStatus, cmw_2: enums.CmwSetStatus, cmw_3: enums.CmwSetStatus, cmw_4: enums.CmwSetStatus) -> None:
		"""SCPI: INITiate:BASE:MCMW \n
		Snippet: driver.base.multiCmw.initiate(cmw_1 = enums.CmwSetStatus.MCMW, cmw_2 = enums.CmwSetStatus.MCMW, cmw_3 = enums.CmwSetStatus.MCMW, cmw_4 = enums.CmwSetStatus.MCMW) \n
		No command help available \n
			:param cmw_1: No help available
			:param cmw_2: No help available
			:param cmw_3: No help available
			:param cmw_4: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cmw_1', cmw_1, DataType.Enum), ArgSingle('cmw_2', cmw_2, DataType.Enum), ArgSingle('cmw_3', cmw_3, DataType.Enum), ArgSingle('cmw_4', cmw_4, DataType.Enum))
		self._core.io.write(f'INITiate:BASE:MCMW {param}'.rstrip())

	def clone(self) -> 'MultiCmw':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MultiCmw(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
