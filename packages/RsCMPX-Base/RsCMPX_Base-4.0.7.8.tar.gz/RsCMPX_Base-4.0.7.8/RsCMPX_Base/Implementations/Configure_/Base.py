from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Base:
	"""Base commands group definition. 26 total commands, 8 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("base", core, parent)

	@property
	def multiCmw(self):
		"""multiCmw commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_multiCmw'):
			from .Base_.MultiCmw import MultiCmw
			self._multiCmw = MultiCmw(self._core, self._base)
		return self._multiCmw

	@property
	def ipSubnet(self):
		"""ipSubnet commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ipSubnet'):
			from .Base_.IpSubnet import IpSubnet
			self._ipSubnet = IpSubnet(self._core, self._base)
		return self._ipSubnet

	@property
	def adjustment(self):
		"""adjustment commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_adjustment'):
			from .Base_.Adjustment import Adjustment
			self._adjustment = Adjustment(self._core, self._base)
		return self._adjustment

	@property
	def ipcr(self):
		"""ipcr commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ipcr'):
			from .Base_.Ipcr import Ipcr
			self._ipcr = Ipcr(self._core, self._base)
		return self._ipcr

	@property
	def freqCorrection(self):
		"""freqCorrection commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_freqCorrection'):
			from .Base_.FreqCorrection import FreqCorrection
			self._freqCorrection = FreqCorrection(self._core, self._base)
		return self._freqCorrection

	@property
	def correction(self):
		"""correction commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_correction'):
			from .Base_.Correction import Correction
			self._correction = Correction(self._core, self._base)
		return self._correction

	@property
	def mmonitor(self):
		"""mmonitor commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mmonitor'):
			from .Base_.Mmonitor import Mmonitor
			self._mmonitor = Mmonitor(self._core, self._base)
		return self._mmonitor

	@property
	def salignment(self):
		"""salignment commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_salignment'):
			from .Base_.Salignment import Salignment
			self._salignment = Salignment(self._core, self._base)
		return self._salignment

	# noinspection PyTypeChecker
	def get_fcontrol(self) -> enums.FanMode:
		"""SCPI: CONFigure:BASE:FCONtrol \n
		Snippet: value: enums.FanMode = driver.configure.base.get_fcontrol() \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('CONFigure:BASE:FCONtrol?')
		return Conversions.str_to_scalar_enum(response, enums.FanMode)

	def set_fcontrol(self, mode: enums.FanMode) -> None:
		"""SCPI: CONFigure:BASE:FCONtrol \n
		Snippet: driver.configure.base.set_fcontrol(mode = enums.FanMode.HIGH) \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FanMode)
		self._core.io.write(f'CONFigure:BASE:FCONtrol {param}')

	def clone(self) -> 'Base':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Base(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
