from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.Utilities import trim_str_response
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def set(self, board: str, tableid: int, board_instance: int = None) -> None:
		"""SCPI: DIAGnostic:EEPRom:DATA \n
		Snippet: driver.diagnostic.eeprom.data.set(board = '1', tableid = 1, board_instance = 1) \n
		No command help available \n
			:param board: No help available
			:param tableid: No help available
			:param board_instance: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('board', board, DataType.String), ArgSingle('tableid', tableid, DataType.Integer), ArgSingle('board_instance', board_instance, DataType.Integer, True))
		self._core.io.write(f'DIAGnostic:EEPRom:DATA {param}'.rstrip())

	def get(self) -> str:
		"""SCPI: DIAGnostic:EEPRom:DATA \n
		Snippet: value: str = driver.diagnostic.eeprom.data.get() \n
		No command help available \n
			:return: datafolder: No help available"""
		response = self._core.io.query_str(f'DIAGnostic:EEPRom:DATA?')
		return trim_str_response(response)
