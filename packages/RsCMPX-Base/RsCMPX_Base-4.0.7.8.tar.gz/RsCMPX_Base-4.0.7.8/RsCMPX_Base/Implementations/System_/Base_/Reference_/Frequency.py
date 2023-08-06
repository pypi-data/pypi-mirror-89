from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 3 total commands, 1 Sub-groups, 2 group commands
	Repeated Capability: Frequency, default value after init: Frequency.Freq1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_frequency_get', 'repcap_frequency_set', repcap.Frequency.Freq1)

	def repcap_frequency_set(self, enum_value: repcap.Frequency) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Frequency.Default
		Default value after init: Frequency.Freq1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_frequency_get(self) -> repcap.Frequency:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def advanced(self):
		"""advanced commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_advanced'):
			from .Frequency_.Advanced import Advanced
			self._advanced = Advanced(self._core, self._base)
		return self._advanced

	# noinspection PyTypeChecker
	def get_source(self) -> enums.SourceIntExt:
		"""SCPI: SYSTem:BASE:REFerence:FREQuency:SOURce \n
		Snippet: value: enums.SourceIntExt = driver.system.base.reference.frequency.get_source() \n
		Selects the reference frequency source to be used. \n
			:return: source: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:REFerence:FREQuency:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SourceIntExt)

	def set_source(self, source: enums.SourceIntExt) -> None:
		"""SCPI: SYSTem:BASE:REFerence:FREQuency:SOURce \n
		Snippet: driver.system.base.reference.frequency.set_source(source = enums.SourceIntExt.EINTernal) \n
		Selects the reference frequency source to be used. \n
			:param source: INTernal: Internal reference frequency EXTernal: External reference frequency
		"""
		param = Conversions.enum_scalar_to_str(source, enums.SourceIntExt)
		self._core.io.write(f'SYSTem:BASE:REFerence:FREQuency:SOURce {param}')

	def get_value(self) -> float:
		"""SCPI: SYSTem:BASE:REFerence:FREQuency \n
		Snippet: value: float = driver.system.base.reference.frequency.get_value() \n
		Sets the R&S CMX500 external reference frequency. \n
			:return: ref_frequency: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:REFerence:FREQuency?')
		return Conversions.str_to_float(response)

	def set_value(self, ref_frequency: float) -> None:
		"""SCPI: SYSTem:BASE:REFerence:FREQuency \n
		Snippet: driver.system.base.reference.frequency.set_value(ref_frequency = 1.0) \n
		Sets the R&S CMX500 external reference frequency. \n
			:param ref_frequency: No help available
		"""
		param = Conversions.decimal_value_to_str(ref_frequency)
		self._core.io.write(f'SYSTem:BASE:REFerence:FREQuency {param}')

	def clone(self) -> 'Frequency':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frequency(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
