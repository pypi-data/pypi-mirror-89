from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Types import DataType
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FreqCorrection:
	"""FreqCorrection commands group definition. 4 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("freqCorrection", core, parent)

	@property
	def activate(self):
		"""activate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_activate'):
			from .FreqCorrection_.Activate import Activate
			self._activate = Activate(self._core, self._base)
		return self._activate

	@property
	def usage(self):
		"""usage commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_usage'):
			from .FreqCorrection_.Usage import Usage
			self._usage = Usage(self._core, self._base)
		return self._usage

	def deactivate(self, connector: str, direction: enums.RxTxDirection = None, rf_converter: enums.RfConverterInPath = None) -> None:
		"""SCPI: CONFigure:FDCorrection:DEACtivate \n
		Snippet: driver.configure.freqCorrection.deactivate(connector = r1, direction = enums.RxTxDirection.RX, rf_converter = enums.RfConverterInPath.RF1) \n
		No command help available \n
			:param connector: No help available
			:param direction: No help available
			:param rf_converter: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('connector', connector, DataType.RawString), ArgSingle('direction', direction, DataType.Enum, True), ArgSingle('rf_converter', rf_converter, DataType.Enum, True))
		self._core.io.write(f'CONFigure:FDCorrection:DEACtivate {param}'.rstrip())

	def deactivate_all(self, direction: enums.RxTxDirection = None, table_path: str = None) -> None:
		"""SCPI: CONFigure:FDCorrection:DEACtivate:ALL \n
		Snippet: driver.configure.freqCorrection.deactivate_all(direction = enums.RxTxDirection.RX, table_path = '1') \n
		No command help available \n
			:param direction: No help available
			:param table_path: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('direction', direction, DataType.Enum, True), ArgSingle('table_path', table_path, DataType.String, True))
		self._core.io.write(f'CONFigure:FDCorrection:DEACtivate:ALL {param}'.rstrip())

	def clone(self) -> 'FreqCorrection':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FreqCorrection(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
