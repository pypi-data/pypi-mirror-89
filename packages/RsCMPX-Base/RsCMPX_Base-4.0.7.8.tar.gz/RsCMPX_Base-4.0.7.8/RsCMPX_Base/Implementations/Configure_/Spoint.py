from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Spoint:
	"""Spoint commands group definition. 5 total commands, 3 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spoint", core, parent)

	@property
	def define(self):
		"""define commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_define'):
			from .Spoint_.Define import Define
			self._define = Define(self._core, self._base)
		return self._define

	@property
	def rewait(self):
		"""rewait commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rewait'):
			from .Spoint_.Rewait import Rewait
			self._rewait = Rewait(self._core, self._base)
		return self._rewait

	@property
	def join(self):
		"""join commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_join'):
			from .Spoint_.Join import Join
			self._join = Join(self._core, self._base)
		return self._join

	# noinspection PyTypeChecker
	class CatalogStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Name: str: No parameter help available
			- Def_Timeout: int: No parameter help available
			- Def_Count: int: No parameter help available
			- Scope: enums.ValidityScopeA: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_str('Name'),
			ArgStruct.scalar_int('Def_Timeout'),
			ArgStruct.scalar_int('Def_Count'),
			ArgStruct.scalar_enum('Scope', enums.ValidityScopeA)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Name: str = None
			self.Def_Timeout: int = None
			self.Def_Count: int = None
			self.Scope: enums.ValidityScopeA = None

	def get_catalog(self) -> CatalogStruct:
		"""SCPI: CONFigure:SPOint:CATalog \n
		Snippet: value: CatalogStruct = driver.configure.spoint.get_catalog() \n
		No command help available \n
			:return: structure: for return value, see the help for CatalogStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:SPOint:CATalog?', self.__class__.CatalogStruct())

	def set_undefine(self, name: str) -> None:
		"""SCPI: CONFigure:SPOint:UNDefine \n
		Snippet: driver.configure.spoint.set_undefine(name = '1') \n
		No command help available \n
			:param name: No help available
		"""
		param = Conversions.value_to_quoted_str(name)
		self._core.io.write(f'CONFigure:SPOint:UNDefine {param}')

	def clone(self) -> 'Spoint':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Spoint(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
