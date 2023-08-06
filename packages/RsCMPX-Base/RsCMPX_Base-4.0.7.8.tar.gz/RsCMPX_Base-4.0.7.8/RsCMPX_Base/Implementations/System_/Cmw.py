from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cmw:
	"""Cmw commands group definition. 3 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: CmwVariant, default value after init: CmwVariant.Cmw1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cmw", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_cmwVariant_get', 'repcap_cmwVariant_set', repcap.CmwVariant.Cmw1)

	def repcap_cmwVariant_set(self, enum_value: repcap.CmwVariant) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CmwVariant.Default
		Default value after init: CmwVariant.Cmw1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_cmwVariant_get(self) -> repcap.CmwVariant:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def device(self):
		"""device commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_device'):
			from .Cmw_.Device import Device
			self._device = Device(self._core, self._base)
		return self._device

	def clone(self) -> 'Cmw':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cmw(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
