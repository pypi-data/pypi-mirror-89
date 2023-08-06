from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Salignment:
	"""Salignment commands group definition. 23 total commands, 7 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("salignment", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Salignment_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def lvalid(self):
		"""lvalid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lvalid'):
			from .Salignment_.Lvalid import Lvalid
			self._lvalid = Lvalid(self._core, self._base)
		return self._lvalid

	@property
	def reliabiliy(self):
		"""reliabiliy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reliabiliy'):
			from .Salignment_.Reliabiliy import Reliabiliy
			self._reliabiliy = Reliabiliy(self._core, self._base)
		return self._reliabiliy

	@property
	def trace(self):
		"""trace commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_trace'):
			from .Salignment_.Trace import Trace
			self._trace = Trace(self._core, self._base)
		return self._trace

	@property
	def ulimit(self):
		"""ulimit commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ulimit'):
			from .Salignment_.Ulimit import Ulimit
			self._ulimit = Ulimit(self._core, self._base)
		return self._ulimit

	@property
	def llimit(self):
		"""llimit commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_llimit'):
			from .Salignment_.Llimit import Llimit
			self._llimit = Llimit(self._core, self._base)
		return self._llimit

	@property
	def xvalues(self):
		"""xvalues commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_xvalues'):
			from .Salignment_.Xvalues import Xvalues
			self._xvalues = Xvalues(self._core, self._base)
		return self._xvalues

	def initiate(self) -> None:
		"""SCPI: INITiate:BASE:SALignment \n
		Snippet: driver.base.salignment.initiate() \n
		Starts the measurement procedure. \n
		"""
		self._core.io.write(f'INITiate:BASE:SALignment')

	def initiate_with_opc(self) -> None:
		"""SCPI: INITiate:BASE:SALignment \n
		Snippet: driver.base.salignment.initiate_with_opc() \n
		Starts the measurement procedure. \n
		Same as initiate, but waits for the operation to complete before continuing further. Use the RsCMPX_Base.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'INITiate:BASE:SALignment')

	def abort(self) -> None:
		"""SCPI: ABORt:BASE:SALignment \n
		Snippet: driver.base.salignment.abort() \n
		Aborts the measurement procedure. \n
		"""
		self._core.io.write(f'ABORt:BASE:SALignment')

	def abort_with_opc(self) -> None:
		"""SCPI: ABORt:BASE:SALignment \n
		Snippet: driver.base.salignment.abort_with_opc() \n
		Aborts the measurement procedure. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCMPX_Base.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ABORt:BASE:SALignment')

	def stop(self) -> None:
		"""SCPI: STOP:BASE:SALignment \n
		Snippet: driver.base.salignment.stop() \n
		Pauses the measurement procedure. \n
		"""
		self._core.io.write(f'STOP:BASE:SALignment')

	def stop_with_opc(self) -> None:
		"""SCPI: STOP:BASE:SALignment \n
		Snippet: driver.base.salignment.stop_with_opc() \n
		Pauses the measurement procedure. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCMPX_Base.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'STOP:BASE:SALignment')

	# noinspection PyTypeChecker
	def fetch(self) -> enums.ResourceState:
		"""SCPI: FETCh:BASE:SALignment \n
		Snippet: value: enums.ResourceState = driver.base.salignment.fetch() \n
		Queries the state of the measurement procedure. \n
			:return: meas_status: OFF: measurement off RUN: measurement running RDY: measurement finished"""
		response = self._core.io.query_str(f'FETCh:BASE:SALignment?')
		return Conversions.str_to_scalar_enum(response, enums.ResourceState)

	def clone(self) -> 'Salignment':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Salignment(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
