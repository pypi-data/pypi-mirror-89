from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Define:
	"""Define commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("define", core, parent)

	def set(self, name: str, timeout: float, scope: enums.ValidityScopeA = None) -> None:
		"""SCPI: CONFigure:MUTex:DEFine \n
		Snippet: driver.configure.mutex.define.set(name = '1', timeout = 1.0, scope = enums.ValidityScopeA.GLOBal) \n
		No command help available \n
			:param name: No help available
			:param timeout: No help available
			:param scope: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('name', name, DataType.String), ArgSingle('timeout', timeout, DataType.Float), ArgSingle('scope', scope, DataType.Enum, True))
		self._core.io.write(f'CONFigure:MUTex:DEFine {param}'.rstrip())
