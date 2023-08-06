from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Slot:
	"""Slot commands group definition. 2 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: Slot, default value after init: Slot.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("slot", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_slot_get', 'repcap_slot_set', repcap.Slot.Nr1)

	def repcap_slot_set(self, enum_value: repcap.Slot) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Slot.Default
		Default value after init: Slot.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_slot_get(self) -> repcap.Slot:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def rxFilter(self):
		"""rxFilter commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rxFilter'):
			from .Slot_.RxFilter import RxFilter
			self._rxFilter = RxFilter(self._core, self._base)
		return self._rxFilter

	@property
	def txFilter(self):
		"""txFilter commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_txFilter'):
			from .Slot_.TxFilter import TxFilter
			self._txFilter = TxFilter(self._core, self._base)
		return self._txFilter

	def clone(self) -> 'Slot':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Slot(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
