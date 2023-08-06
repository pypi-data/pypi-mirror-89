from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NwAdapter:
	"""NwAdapter commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: NwAdapter, default value after init: NwAdapter.Adapter1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nwAdapter", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_nwAdapter_get', 'repcap_nwAdapter_set', repcap.NwAdapter.Adapter1)

	def repcap_nwAdapter_set(self, enum_value: repcap.NwAdapter) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to NwAdapter.Default
		Default value after init: NwAdapter.Adapter1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_nwAdapter_get(self) -> repcap.NwAdapter:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, set_subnet_conform: bool, nwAdapter=repcap.NwAdapter.Default) -> None:
		"""SCPI: CONFigure:BASE:IPSet:NWADapter<n> \n
		Snippet: driver.configure.base.ipSubnet.nwAdapter.set(set_subnet_conform = False, nwAdapter = repcap.NwAdapter.Default) \n
		No command help available \n
			:param set_subnet_conform: No help available
			:param nwAdapter: optional repeated capability selector. Default value: Adapter1 (settable in the interface 'NwAdapter')"""
		param = Conversions.bool_to_str(set_subnet_conform)
		nwAdapter_cmd_val = self._base.get_repcap_cmd_value(nwAdapter, repcap.NwAdapter)
		self._core.io.write(f'CONFigure:BASE:IPSet:NWADapter{nwAdapter_cmd_val} {param}')

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Nw_Adapter_Name: str: No parameter help available
			- Set_Subnet_Conform: bool: No parameter help available
			- Ip_Address: str: No parameter help available
			- Status: enums.AdjustStatus: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_str('Nw_Adapter_Name'),
			ArgStruct.scalar_bool('Set_Subnet_Conform'),
			ArgStruct.scalar_str('Ip_Address'),
			ArgStruct.scalar_enum('Status', enums.AdjustStatus)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Nw_Adapter_Name: str = None
			self.Set_Subnet_Conform: bool = None
			self.Ip_Address: str = None
			self.Status: enums.AdjustStatus = None

	def get(self, nwAdapter=repcap.NwAdapter.Default) -> GetStruct:
		"""SCPI: CONFigure:BASE:IPSet:NWADapter<n> \n
		Snippet: value: GetStruct = driver.configure.base.ipSubnet.nwAdapter.get(nwAdapter = repcap.NwAdapter.Default) \n
		No command help available \n
			:param nwAdapter: optional repeated capability selector. Default value: Adapter1 (settable in the interface 'NwAdapter')
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		nwAdapter_cmd_val = self._base.get_repcap_cmd_value(nwAdapter, repcap.NwAdapter)
		return self._core.io.query_struct(f'CONFigure:BASE:IPSet:NWADapter{nwAdapter_cmd_val}?', self.__class__.GetStruct())

	def clone(self) -> 'NwAdapter':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NwAdapter(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
