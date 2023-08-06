from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Event:
	"""Event commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("event", core, parent)

	def get(self, bitNr=repcap.BitNr.Default) -> bool:
		"""SCPI: STATus:OPERation:BIT<bitno>[:EVENt] \n
		Snippet: value: bool = driver.status.operation.bit.event.get(bitNr = repcap.BitNr.Default) \n
		No command help available \n
			:param bitNr: optional repeated capability selector. Default value: Nr8 (settable in the interface 'Bit')
			:return: register_bit: No help available"""
		bitNr_cmd_val = self._base.get_repcap_cmd_value(bitNr, repcap.BitNr)
		response = self._core.io.query_str(f'STATus:OPERation:BIT{bitNr_cmd_val}:EVENt?')
		return Conversions.str_to_bool(response)
