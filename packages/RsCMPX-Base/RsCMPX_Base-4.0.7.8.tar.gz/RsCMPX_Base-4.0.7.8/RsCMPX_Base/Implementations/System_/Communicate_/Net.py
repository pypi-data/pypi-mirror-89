from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Net:
	"""Net commands group definition. 8 total commands, 2 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("net", core, parent)

	@property
	def dns(self):
		"""dns commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_dns'):
			from .Net_.Dns import Dns
			self._dns = Dns(self._core, self._base)
		return self._dns

	@property
	def subnet(self):
		"""subnet commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subnet'):
			from .Net_.Subnet import Subnet
			self._subnet = Subnet(self._core, self._base)
		return self._subnet

	def get_adapter(self) -> str:
		"""SCPI: SYSTem:COMMunicate:NET:ADAPter \n
		Snippet: value: str = driver.system.communicate.net.get_adapter() \n
		Selects a LAN network adapter for configuration via other SYSTem:COMMunicate:NET... commands. \n
			:return: networkadapter: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NET:ADAPter?')
		return trim_str_response(response)

	def set_adapter(self, networkadapter: str) -> None:
		"""SCPI: SYSTem:COMMunicate:NET:ADAPter \n
		Snippet: driver.system.communicate.net.set_adapter(networkadapter = '1') \n
		Selects a LAN network adapter for configuration via other SYSTem:COMMunicate:NET... commands. \n
			:param networkadapter: No help available
		"""
		param = Conversions.value_to_quoted_str(networkadapter)
		self._core.io.write(f'SYSTem:COMMunicate:NET:ADAPter {param}')

	def get_gateway(self) -> List[str]:
		"""SCPI: SYSTem:COMMunicate:NET:GATeway \n
		Snippet: value: List[str] = driver.system.communicate.net.get_gateway() \n
		Manually defines IPv4 addresses of default gateways. A query returns the currently defined addresses, irrespective of
		whether they have been specified manually or via DHCP. \n
			:return: gateways: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NET:GATeway?')
		return Conversions.str_to_str_list(response)

	def set_gateway(self, gateways: List[str]) -> None:
		"""SCPI: SYSTem:COMMunicate:NET:GATeway \n
		Snippet: driver.system.communicate.net.set_gateway(gateways = ['1', '2', '3']) \n
		Manually defines IPv4 addresses of default gateways. A query returns the currently defined addresses, irrespective of
		whether they have been specified manually or via DHCP. \n
			:param gateways: Gateway IPv4 address consisting of four blocks separated by dots Several strings separated by commas can be entered or several addresses separated by commas can be included in one string.
		"""
		param = Conversions.list_to_csv_quoted_str(gateways)
		self._core.io.write(f'SYSTem:COMMunicate:NET:GATeway {param}')

	def get_ip_address(self) -> List[str]:
		"""SCPI: SYSTem:COMMunicate:NET:IPADdress \n
		Snippet: value: List[str] = driver.system.communicate.net.get_ip_address() \n
		Manually assigns one or more IPv4 addresses to the network adapter. A query returns the currently assigned addresses,
		irrespective of whether they have been assigned manually or via DHCP. \n
			:return: ipaddresses: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NET:IPADdress?')
		return Conversions.str_to_str_list(response)

	def set_ip_address(self, ipaddresses: List[str]) -> None:
		"""SCPI: SYSTem:COMMunicate:NET:IPADdress \n
		Snippet: driver.system.communicate.net.set_ip_address(ipaddresses = ['1', '2', '3']) \n
		Manually assigns one or more IPv4 addresses to the network adapter. A query returns the currently assigned addresses,
		irrespective of whether they have been assigned manually or via DHCP. \n
			:param ipaddresses: IPv4 address consisting of four blocks (octets) separated by dots Several strings separated by commas can be entered or several addresses separated by commas can be included in one string.
		"""
		param = Conversions.list_to_csv_quoted_str(ipaddresses)
		self._core.io.write(f'SYSTem:COMMunicate:NET:IPADdress {param}')

	def get_hostname(self) -> str:
		"""SCPI: SYSTem:COMMunicate:NET:HOSTname \n
		Snippet: value: str = driver.system.communicate.net.get_hostname() \n
		Queries the host name (computer name) of the R&S CMX500. The host name is part of the VISA address string for LAN-based
		connections. \n
			:return: hostname: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NET:HOSTname?')
		return trim_str_response(response)

	def set_hostname(self, hostname: str) -> None:
		"""SCPI: SYSTem:COMMunicate:NET:HOSTname \n
		Snippet: driver.system.communicate.net.set_hostname(hostname = '1') \n
		Queries the host name (computer name) of the R&S CMX500. The host name is part of the VISA address string for LAN-based
		connections. \n
			:param hostname: No help available
		"""
		param = Conversions.value_to_quoted_str(hostname)
		self._core.io.write(f'SYSTem:COMMunicate:NET:HOSTname {param}')

	def get_dhcp(self) -> bool:
		"""SCPI: SYSTem:COMMunicate:NET:DHCP \n
		Snippet: value: bool = driver.system.communicate.net.get_dhcp() \n
		No command help available \n
			:return: dhcp_enable: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NET:DHCP?')
		return Conversions.str_to_bool(response)

	def set_dhcp(self, dhcp_enable: bool) -> None:
		"""SCPI: SYSTem:COMMunicate:NET:DHCP \n
		Snippet: driver.system.communicate.net.set_dhcp(dhcp_enable = False) \n
		No command help available \n
			:param dhcp_enable: No help available
		"""
		param = Conversions.bool_to_str(dhcp_enable)
		self._core.io.write(f'SYSTem:COMMunicate:NET:DHCP {param}')

	def clone(self) -> 'Net':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Net(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
