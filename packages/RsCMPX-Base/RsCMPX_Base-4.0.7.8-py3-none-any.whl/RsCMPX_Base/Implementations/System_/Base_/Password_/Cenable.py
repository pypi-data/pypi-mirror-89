from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cenable:
	"""Cenable commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cenable", core, parent)

	# noinspection PyTypeChecker
	def get_state(self) -> enums.UserRole:
		"""SCPI: SYSTem:BASE:PASSword[:CENable]:STATe \n
		Snippet: value: enums.UserRole = driver.system.base.password.cenable.get_state() \n
		No command help available \n
			:return: usermode: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:PASSword:CENable:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.UserRole)

	def set(self, usermode: enums.UserRole, password: str) -> None:
		"""SCPI: SYSTem:BASE:PASSword[:CENable] \n
		Snippet: driver.system.base.password.cenable.set(usermode = enums.UserRole.ADMin, password = '1') \n
		No command help available \n
			:param usermode: No help available
			:param password: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('usermode', usermode, DataType.Enum), ArgSingle('password', password, DataType.String))
		self._core.io.write(f'SYSTem:BASE:PASSword:CENable {param}'.rstrip())
