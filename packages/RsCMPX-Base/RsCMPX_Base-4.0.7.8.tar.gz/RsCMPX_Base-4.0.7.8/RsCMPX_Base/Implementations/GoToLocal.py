from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GoToLocal:
	"""GoToLocal commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("goToLocal", core, parent)

	def set(self) -> None:
		"""SCPI: *GTL \n
		Snippet: driver.goToLocal.set() \n
		No command help available \n
		"""
		self._core.io.write(f'*GTL')

	def set_with_opc(self) -> None:
		"""SCPI: *GTL \n
		Snippet: driver.goToLocal.set_with_opc() \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCMPX_Base.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'*GTL')
