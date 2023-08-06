from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Connect:
	"""Connect commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("connect", core, parent)

	@property
	def multiple(self):
		"""multiple commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_multiple'):
			from .Connect_.Multiple import Multiple
			self._multiple = Multiple(self._core, self._base)
		return self._multiple

	def get(self, handle: str, pias_id: str) -> int:
		"""SCPI: DIAGnostic:PIAS:CONNect \n
		Snippet: value: int = driver.diagnostic.pias.connect.get(handle = '1', pias_id = '1') \n
		No command help available \n
			:param handle: No help available
			:param pias_id: No help available
			:return: result: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('handle', handle, DataType.String), ArgSingle('pias_id', pias_id, DataType.String))
		response = self._core.io.query_str(f'DIAGnostic:PIAS:CONNect? {param}'.rstrip())
		return Conversions.str_to_int(response)

	def clone(self) -> 'Connect':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Connect(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
