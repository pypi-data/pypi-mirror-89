from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gpib:
	"""Gpib commands group definition. 3 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: GpibInstance, default value after init: GpibInstance.Inst1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gpib", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_gpibInstance_get', 'repcap_gpibInstance_set', repcap.GpibInstance.Inst1)

	def repcap_gpibInstance_set(self, enum_value: repcap.GpibInstance) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to GpibInstance.Default
		Default value after init: GpibInstance.Inst1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_gpibInstance_get(self) -> repcap.GpibInstance:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def self(self):
		"""self commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_self'):
			from .Gpib_.Self import Self
			self._self = Self(self._core, self._base)
		return self._self

	@property
	def vresource(self):
		"""vresource commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vresource'):
			from .Gpib_.Vresource import Vresource
			self._vresource = Vresource(self._core, self._base)
		return self._vresource

	def clone(self) -> 'Gpib':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Gpib(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
