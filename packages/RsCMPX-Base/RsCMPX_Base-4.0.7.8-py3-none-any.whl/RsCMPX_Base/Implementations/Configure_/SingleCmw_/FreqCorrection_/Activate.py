from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Activate:
	"""Activate commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("activate", core, parent)

	# noinspection PyTypeChecker
	class RxStruct(StructBase):
		"""Structure for setting input parameters. Contains optional set arguments. Fields: \n
			- Connectorbench: str: No parameter help available
			- Table_1: str: No parameter help available
			- Table_2: str: No parameter help available
			- Table_3: str: No parameter help available
			- Table_4: str: No parameter help available
			- Table_5: str: No parameter help available
			- Table_6: str: No parameter help available
			- Table_7: str: No parameter help available
			- Table_8: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Connectorbench'),
			ArgStruct.scalar_str('Table_1'),
			ArgStruct.scalar_str_optional('Table_2'),
			ArgStruct.scalar_str_optional('Table_3'),
			ArgStruct.scalar_str_optional('Table_4'),
			ArgStruct.scalar_str_optional('Table_5'),
			ArgStruct.scalar_str_optional('Table_6'),
			ArgStruct.scalar_str_optional('Table_7'),
			ArgStruct.scalar_str_optional('Table_8')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Connectorbench: str = None
			self.Table_1: str = None
			self.Table_2: str = None
			self.Table_3: str = None
			self.Table_4: str = None
			self.Table_5: str = None
			self.Table_6: str = None
			self.Table_7: str = None
			self.Table_8: str = None

	def set_rx(self, value: RxStruct) -> None:
		"""SCPI: CONFigure:CMWS:FDCorrection:ACTivate:RX \n
		Snippet: driver.configure.singleCmw.freqCorrection.activate.set_rx(value = RxStruct()) \n
		No command help available \n
			:param value: see the help for RxStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:CMWS:FDCorrection:ACTivate:RX', value)

	# noinspection PyTypeChecker
	class TxStruct(StructBase):
		"""Structure for setting input parameters. Contains optional set arguments. Fields: \n
			- Connectorbench: str: No parameter help available
			- Table_1: str: No parameter help available
			- Table_2: str: No parameter help available
			- Table_3: str: No parameter help available
			- Table_4: str: No parameter help available
			- Table_5: str: No parameter help available
			- Table_6: str: No parameter help available
			- Table_7: str: No parameter help available
			- Table_8: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_raw_str('Connectorbench'),
			ArgStruct.scalar_str('Table_1'),
			ArgStruct.scalar_str_optional('Table_2'),
			ArgStruct.scalar_str_optional('Table_3'),
			ArgStruct.scalar_str_optional('Table_4'),
			ArgStruct.scalar_str_optional('Table_5'),
			ArgStruct.scalar_str_optional('Table_6'),
			ArgStruct.scalar_str_optional('Table_7'),
			ArgStruct.scalar_str_optional('Table_8')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Connectorbench: str = None
			self.Table_1: str = None
			self.Table_2: str = None
			self.Table_3: str = None
			self.Table_4: str = None
			self.Table_5: str = None
			self.Table_6: str = None
			self.Table_7: str = None
			self.Table_8: str = None

	def set_tx(self, value: TxStruct) -> None:
		"""SCPI: CONFigure:CMWS:FDCorrection:ACTivate:TX \n
		Snippet: driver.configure.singleCmw.freqCorrection.activate.set_tx(value = TxStruct()) \n
		No command help available \n
			:param value: see the help for TxStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:CMWS:FDCorrection:ACTivate:TX', value)
