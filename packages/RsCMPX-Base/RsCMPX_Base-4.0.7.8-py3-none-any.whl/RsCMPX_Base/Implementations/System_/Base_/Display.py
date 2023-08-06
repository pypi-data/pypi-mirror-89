from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Display:
	"""Display commands group definition. 5 total commands, 0 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("display", core, parent)

	def get_mwindow(self) -> bool:
		"""SCPI: SYSTem:BASE:DISPlay:MWINdow \n
		Snippet: value: bool = driver.system.base.display.get_mwindow() \n
		No command help available \n
			:return: on_off: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:DISPlay:MWINdow?')
		return Conversions.str_to_bool(response)

	def set_mwindow(self, on_off: bool) -> None:
		"""SCPI: SYSTem:BASE:DISPlay:MWINdow \n
		Snippet: driver.system.base.display.set_mwindow(on_off = False) \n
		No command help available \n
			:param on_off: No help available
		"""
		param = Conversions.bool_to_str(on_off)
		self._core.io.write(f'SYSTem:BASE:DISPlay:MWINdow {param}')

	# noinspection PyTypeChecker
	def get_color_set(self) -> enums.ColorSet:
		"""SCPI: SYSTem:BASE:DISPlay:COLorset \n
		Snippet: value: enums.ColorSet = driver.system.base.display.get_color_set() \n
		No command help available \n
			:return: colorset: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:DISPlay:COLorset?')
		return Conversions.str_to_scalar_enum(response, enums.ColorSet)

	def set_color_set(self, colorset: enums.ColorSet) -> None:
		"""SCPI: SYSTem:BASE:DISPlay:COLorset \n
		Snippet: driver.system.base.display.set_color_set(colorset = enums.ColorSet.DEF) \n
		No command help available \n
			:param colorset: No help available
		"""
		param = Conversions.enum_scalar_to_str(colorset, enums.ColorSet)
		self._core.io.write(f'SYSTem:BASE:DISPlay:COLorset {param}')

	# noinspection PyTypeChecker
	def get_font_set(self) -> enums.FontType:
		"""SCPI: SYSTem:BASE:DISPlay:FONTset \n
		Snippet: value: enums.FontType = driver.system.base.display.get_font_set() \n
		No command help available \n
			:return: fonset: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:DISPlay:FONTset?')
		return Conversions.str_to_scalar_enum(response, enums.FontType)

	def set_font_set(self, fonset: enums.FontType) -> None:
		"""SCPI: SYSTem:BASE:DISPlay:FONTset \n
		Snippet: driver.system.base.display.set_font_set(fonset = enums.FontType.DEF) \n
		No command help available \n
			:param fonset: No help available
		"""
		param = Conversions.enum_scalar_to_str(fonset, enums.FontType)
		self._core.io.write(f'SYSTem:BASE:DISPlay:FONTset {param}')

	# noinspection PyTypeChecker
	def get_roll_keymode(self) -> enums.RollkeyMode:
		"""SCPI: SYSTem:BASE:DISPlay:ROLLkeymode \n
		Snippet: value: enums.RollkeyMode = driver.system.base.display.get_roll_keymode() \n
		No command help available \n
			:return: rollkeymode: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:DISPlay:ROLLkeymode?')
		return Conversions.str_to_scalar_enum(response, enums.RollkeyMode)

	def set_roll_keymode(self, rollkeymode: enums.RollkeyMode) -> None:
		"""SCPI: SYSTem:BASE:DISPlay:ROLLkeymode \n
		Snippet: driver.system.base.display.set_roll_keymode(rollkeymode = enums.RollkeyMode.CURSors) \n
		No command help available \n
			:param rollkeymode: No help available
		"""
		param = Conversions.enum_scalar_to_str(rollkeymode, enums.RollkeyMode)
		self._core.io.write(f'SYSTem:BASE:DISPlay:ROLLkeymode {param}')

	# noinspection PyTypeChecker
	def get_language(self) -> enums.DisplayLanguage:
		"""SCPI: SYSTem:BASE:DISPlay:LANGuage \n
		Snippet: value: enums.DisplayLanguage = driver.system.base.display.get_language() \n
		No command help available \n
			:return: language: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:DISPlay:LANGuage?')
		return Conversions.str_to_scalar_enum(response, enums.DisplayLanguage)

	def set_language(self, language: enums.DisplayLanguage) -> None:
		"""SCPI: SYSTem:BASE:DISPlay:LANGuage \n
		Snippet: driver.system.base.display.set_language(language = enums.DisplayLanguage.AR) \n
		No command help available \n
			:param language: No help available
		"""
		param = Conversions.enum_scalar_to_str(language, enums.DisplayLanguage)
		self._core.io.write(f'SYSTem:BASE:DISPlay:LANGuage {param}')
