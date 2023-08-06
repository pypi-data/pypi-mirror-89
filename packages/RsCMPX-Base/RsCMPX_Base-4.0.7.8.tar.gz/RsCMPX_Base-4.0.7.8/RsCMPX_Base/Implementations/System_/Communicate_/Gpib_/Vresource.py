from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Utilities import trim_str_response
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vresource:
	"""Vresource commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("vresource", core, parent)

	def get(self, gpibInstance=repcap.GpibInstance.Default) -> str:
		"""SCPI: SYSTem:COMMunicate:GPIB<inst>:VRESource \n
		Snippet: value: str = driver.system.communicate.gpib.vresource.get(gpibInstance = repcap.GpibInstance.Default) \n
		No command help available \n
			:param gpibInstance: optional repeated capability selector. Default value: Inst1 (settable in the interface 'Gpib')
			:return: visaresource: No help available"""
		gpibInstance_cmd_val = self._base.get_repcap_cmd_value(gpibInstance, repcap.GpibInstance)
		response = self._core.io.query_str(f'SYSTem:COMMunicate:GPIB{gpibInstance_cmd_val}:VRESource?')
		return trim_str_response(response)
