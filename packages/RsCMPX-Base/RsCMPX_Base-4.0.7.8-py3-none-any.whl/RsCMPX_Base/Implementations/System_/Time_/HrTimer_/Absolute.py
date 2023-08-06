from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Absolute:
	"""Absolute commands group definition. 3 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("absolute", core, parent)

	@property
	def set(self):
		"""set commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_set'):
			from .Absolute_.Set import Set
			self._set = Set(self._core, self._base)
		return self._set

	def clear(self) -> None:
		"""SCPI: SYSTem:TIME:HRTimer:ABSolute:CLEar \n
		Snippet: driver.system.time.hrTimer.absolute.clear() \n
		No command help available \n
		"""
		self._core.io.write(f'SYSTem:TIME:HRTimer:ABSolute:CLEar')

	def clear_with_opc(self) -> None:
		"""SCPI: SYSTem:TIME:HRTimer:ABSolute:CLEar \n
		Snippet: driver.system.time.hrTimer.absolute.clear_with_opc() \n
		No command help available \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsCMPX_Base.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:TIME:HRTimer:ABSolute:CLEar')

	def set_value(self, duration: float) -> None:
		"""SCPI: SYSTem:TIME:HRTimer:ABSolute \n
		Snippet: driver.system.time.hrTimer.absolute.set_value(duration = 1.0) \n
		This command starts a timer. The timeout is specified relative to an already set timestamp, see method RsCMPX_Base.System.
		Time.HrTimer.Absolute.Set.set. When the timer expires, 'Operation Complete' is indicated. This event can be evaluated by
		polling, via a *OPC? or via *WAI. \n
			:param duration: No help available
		"""
		param = Conversions.decimal_value_to_str(duration)
		self._core.io.write_with_opc(f'SYSTem:TIME:HRTimer:ABSolute {param}')

	def clone(self) -> 'Absolute':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Absolute(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
