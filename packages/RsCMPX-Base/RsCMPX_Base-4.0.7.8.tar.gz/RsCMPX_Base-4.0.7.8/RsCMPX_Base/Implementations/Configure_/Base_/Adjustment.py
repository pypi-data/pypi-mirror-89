from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Adjustment:
	"""Adjustment commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("adjustment", core, parent)

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.OscillatorType:
		"""SCPI: CONFigure:BASE:ADJustment:TYPE \n
		Snippet: value: enums.OscillatorType = driver.configure.base.adjustment.get_type_py() \n
		No command help available \n
			:return: adj_type: No help available
		"""
		response = self._core.io.query_str('CONFigure:BASE:ADJustment:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.OscillatorType)

	def get_value(self) -> float:
		"""SCPI: CONFigure:BASE:ADJustment:VALue \n
		Snippet: value: float = driver.configure.base.adjustment.get_value() \n
		No command help available \n
			:return: adj_value: No help available
		"""
		response = self._core.io.query_str('CONFigure:BASE:ADJustment:VALue?')
		return Conversions.str_to_float(response)

	def set_value(self, adj_value: float) -> None:
		"""SCPI: CONFigure:BASE:ADJustment:VALue \n
		Snippet: driver.configure.base.adjustment.set_value(adj_value = 1.0) \n
		No command help available \n
			:param adj_value: No help available
		"""
		param = Conversions.decimal_value_to_str(adj_value)
		self._core.io.write(f'CONFigure:BASE:ADJustment:VALue {param}')

	def save(self) -> None:
		"""SCPI: CONFigure:BASE:ADJustment:SAVE \n
		Snippet: driver.configure.base.adjustment.save() \n
		No command help available \n
		"""
		self._core.io.write(f'CONFigure:BASE:ADJustment:SAVE')

	def save_with_opc(self) -> None:
		"""SCPI: CONFigure:BASE:ADJustment:SAVE \n
		Snippet: driver.configure.base.adjustment.save_with_opc() \n
		No command help available \n
		Same as save, but waits for the operation to complete before continuing further. Use the RsCMPX_Base.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CONFigure:BASE:ADJustment:SAVE')
