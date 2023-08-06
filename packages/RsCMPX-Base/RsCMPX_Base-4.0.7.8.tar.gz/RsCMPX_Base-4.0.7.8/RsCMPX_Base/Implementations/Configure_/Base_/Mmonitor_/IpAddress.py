from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IpAddress:
	"""IpAddress commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: IpAddress, default value after init: IpAddress.Addr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ipAddress", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_ipAddress_get', 'repcap_ipAddress_set', repcap.IpAddress.Addr1)

	def repcap_ipAddress_set(self, enum_value: repcap.IpAddress) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to IpAddress.Default
		Default value after init: IpAddress.Addr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_ipAddress_get(self) -> repcap.IpAddress:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	# noinspection PyTypeChecker
	class IpAddressStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- First_Segment: int: No parameter help available
			- Second_Segment: int: No parameter help available
			- System_Id: int: No parameter help available
			- Local_Id: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('First_Segment'),
			ArgStruct.scalar_int('Second_Segment'),
			ArgStruct.scalar_int('System_Id'),
			ArgStruct.scalar_int('Local_Id')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.First_Segment: int = None
			self.Second_Segment: int = None
			self.System_Id: int = None
			self.Local_Id: int = None

	def set(self, structure: IpAddressStruct, ipAddress=repcap.IpAddress.Default) -> None:
		"""SCPI: CONFigure:BASE:MMONitor:IPADdress<n> \n
		Snippet: driver.configure.base.mmonitor.ipAddress.set(value = [PROPERTY_STRUCT_NAME](), ipAddress = repcap.IpAddress.Default) \n
		No command help available \n
			:param structure: for set value, see the help for IpAddressStruct structure arguments.
			:param ipAddress: optional repeated capability selector. Default value: Addr1 (settable in the interface 'IpAddress')"""
		ipAddress_cmd_val = self._base.get_repcap_cmd_value(ipAddress, repcap.IpAddress)
		self._core.io.write_struct(f'CONFigure:BASE:MMONitor:IPADdress{ipAddress_cmd_val}', structure)

	def get(self, ipAddress=repcap.IpAddress.Default) -> IpAddressStruct:
		"""SCPI: CONFigure:BASE:MMONitor:IPADdress<n> \n
		Snippet: value: IpAddressStruct = driver.configure.base.mmonitor.ipAddress.get(ipAddress = repcap.IpAddress.Default) \n
		No command help available \n
			:param ipAddress: optional repeated capability selector. Default value: Addr1 (settable in the interface 'IpAddress')
			:return: structure: for return value, see the help for IpAddressStruct structure arguments."""
		ipAddress_cmd_val = self._base.get_repcap_cmd_value(ipAddress, repcap.IpAddress)
		return self._core.io.query_struct(f'CONFigure:BASE:MMONitor:IPADdress{ipAddress_cmd_val}?', self.__class__.IpAddressStruct())

	def clone(self) -> 'IpAddress':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IpAddress(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
