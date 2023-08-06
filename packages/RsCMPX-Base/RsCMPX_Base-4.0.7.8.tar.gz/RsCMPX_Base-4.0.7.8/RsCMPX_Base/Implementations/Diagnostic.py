from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Diagnostic:
	"""Diagnostic commands group definition. 63 total commands, 16 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("diagnostic", core, parent)

	@property
	def base(self):
		"""base commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_base'):
			from .Diagnostic_.Base import Base
			self._base = Base(self._core, self._base)
		return self._base

	@property
	def routing(self):
		"""routing commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_routing'):
			from .Diagnostic_.Routing import Routing
			self._routing = Routing(self._core, self._base)
		return self._routing

	@property
	def eeprom(self):
		"""eeprom commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_eeprom'):
			from .Diagnostic_.Eeprom import Eeprom
			self._eeprom = Eeprom(self._core, self._base)
		return self._eeprom

	@property
	def bgInfo(self):
		"""bgInfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bgInfo'):
			from .Diagnostic_.BgInfo import BgInfo
			self._bgInfo = BgInfo(self._core, self._base)
		return self._bgInfo

	@property
	def singleCmw(self):
		"""singleCmw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_singleCmw'):
			from .Diagnostic_.SingleCmw import SingleCmw
			self._singleCmw = SingleCmw(self._core, self._base)
		return self._singleCmw

	@property
	def cmw(self):
		"""cmw commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cmw'):
			from .Diagnostic_.Cmw import Cmw
			self._cmw = Cmw(self._core, self._base)
		return self._cmw

	@property
	def log(self):
		"""log commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_log'):
			from .Diagnostic_.Log import Log
			self._log = Log(self._core, self._base)
		return self._log

	@property
	def footPrint(self):
		"""footPrint commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_footPrint'):
			from .Diagnostic_.FootPrint import FootPrint
			self._footPrint = FootPrint(self._core, self._base)
		return self._footPrint

	@property
	def status(self):
		"""status commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_status'):
			from .Diagnostic_.Status import Status
			self._status = Status(self._core, self._base)
		return self._status

	@property
	def error(self):
		"""error commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_error'):
			from .Diagnostic_.Error import Error
			self._error = Error(self._core, self._base)
		return self._error

	@property
	def help(self):
		"""help commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_help'):
			from .Diagnostic_.Help import Help
			self._help = Help(self._core, self._base)
		return self._help

	@property
	def instrument(self):
		"""instrument commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_instrument'):
			from .Diagnostic_.Instrument import Instrument
			self._instrument = Instrument(self._core, self._base)
		return self._instrument

	@property
	def compass(self):
		"""compass commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_compass'):
			from .Diagnostic_.Compass import Compass
			self._compass = Compass(self._core, self._base)
		return self._compass

	@property
	def record(self):
		"""record commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_record'):
			from .Diagnostic_.Record import Record
			self._record = Record(self._core, self._base)
		return self._record

	@property
	def pias(self):
		"""pias commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_pias'):
			from .Diagnostic_.Pias import Pias
			self._pias = Pias(self._core, self._base)
		return self._pias

	@property
	def product(self):
		"""product commands group. 2 Sub-classes, 5 commands."""
		if not hasattr(self, '_product'):
			from .Diagnostic_.Product import Product
			self._product = Product(self._core, self._base)
		return self._product

	def set_sdbm(self, text: str) -> None:
		"""SCPI: DIAGnostic:SDBM \n
		Snippet: driver.diagnostic.set_sdbm(text = '1') \n
		No command help available \n
			:param text: No help available
		"""
		param = Conversions.value_to_quoted_str(text)
		self._core.io.write(f'DIAGnostic:SDBM {param}')

	def clone(self) -> 'Diagnostic':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Diagnostic(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
