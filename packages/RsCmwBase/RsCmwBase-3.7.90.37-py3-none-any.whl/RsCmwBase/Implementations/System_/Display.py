from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Display:
	"""Display commands group definition. 8 total commands, 1 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("display", core, parent)

	@property
	def monitor(self):
		"""monitor commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_monitor'):
			from .Display_.Monitor import Monitor
			self._monitor = Monitor(self._core, self._base)
		return self._monitor

	def get_update(self) -> bool:
		"""SCPI: SYSTem:DISPlay:UPDate \n
		Snippet: value: bool = driver.system.display.get_update() \n
		Defines whether the display is updated or not while the instrument is in the remote state. If the display update is
		switched off, the normal GUI is replaced by a static image while the instrument is in the remote state. Switching off the
		display can speed up the measurement and is the recommended state. See also 'Using the Display during Remote Control' \n
			:return: displayupdate: No help available
		"""
		response = self._core.io.query_str('SYSTem:DISPlay:UPDate?')
		return Conversions.str_to_bool(response)

	def set_update(self, displayupdate: bool) -> None:
		"""SCPI: SYSTem:DISPlay:UPDate \n
		Snippet: driver.system.display.set_update(displayupdate = False) \n
		Defines whether the display is updated or not while the instrument is in the remote state. If the display update is
		switched off, the normal GUI is replaced by a static image while the instrument is in the remote state. Switching off the
		display can speed up the measurement and is the recommended state. See also 'Using the Display during Remote Control' \n
			:param displayupdate: ON | 1: Display is shown and updated during remote control. OFF | 0: Display shows static image during remote control.
		"""
		param = Conversions.bool_to_str(displayupdate)
		self._core.io.write(f'SYSTem:DISPlay:UPDate {param}')

	def get_mwindow(self) -> bool:
		"""SCPI: SYSTem:BASE:DISPlay:MWINdow \n
		Snippet: value: bool = driver.system.display.get_mwindow() \n
		Enables or disables the multiple-window mode of the graphical user interface. \n
			:return: on_off: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:DISPlay:MWINdow?')
		return Conversions.str_to_bool(response)

	def set_mwindow(self, on_off: bool) -> None:
		"""SCPI: SYSTem:BASE:DISPlay:MWINdow \n
		Snippet: driver.system.display.set_mwindow(on_off = False) \n
		Enables or disables the multiple-window mode of the graphical user interface. \n
			:param on_off: 0 | 1 1: multiple-window mode 0: single-window mode
		"""
		param = Conversions.bool_to_str(on_off)
		self._core.io.write(f'SYSTem:BASE:DISPlay:MWINdow {param}')

	# noinspection PyTypeChecker
	def get_color_set(self) -> enums.ColorSet:
		"""SCPI: SYSTem:BASE:DISPlay:COLorset \n
		Snippet: value: enums.ColorSet = driver.system.display.get_color_set() \n
		No command help available \n
			:return: colorset: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:DISPlay:COLorset?')
		return Conversions.str_to_scalar_enum(response, enums.ColorSet)

	def set_color_set(self, colorset: enums.ColorSet) -> None:
		"""SCPI: SYSTem:BASE:DISPlay:COLorset \n
		Snippet: driver.system.display.set_color_set(colorset = enums.ColorSet.DEF) \n
		No command help available \n
			:param colorset: No help available
		"""
		param = Conversions.enum_scalar_to_str(colorset, enums.ColorSet)
		self._core.io.write(f'SYSTem:BASE:DISPlay:COLorset {param}')

	# noinspection PyTypeChecker
	def get_font_set(self) -> enums.FontType:
		"""SCPI: SYSTem:BASE:DISPlay:FONTset \n
		Snippet: value: enums.FontType = driver.system.display.get_font_set() \n
		Selects the font size for the GUI labels. \n
			:return: fonset: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:DISPlay:FONTset?')
		return Conversions.str_to_scalar_enum(response, enums.FontType)

	def set_font_set(self, fonset: enums.FontType) -> None:
		"""SCPI: SYSTem:BASE:DISPlay:FONTset \n
		Snippet: driver.system.display.set_font_set(fonset = enums.FontType.DEF) \n
		Selects the font size for the GUI labels. \n
			:param fonset: DEF | LRG DEF: Small fonts LRG: Large fonts
		"""
		param = Conversions.enum_scalar_to_str(fonset, enums.FontType)
		self._core.io.write(f'SYSTem:BASE:DISPlay:FONTset {param}')

	# noinspection PyTypeChecker
	def get_roll_keymode(self) -> enums.RollkeyMode:
		"""SCPI: SYSTem:BASE:DISPlay:ROLLkeymode \n
		Snippet: value: enums.RollkeyMode = driver.system.display.get_roll_keymode() \n
		No command help available \n
			:return: rollkeymode: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:DISPlay:ROLLkeymode?')
		return Conversions.str_to_scalar_enum(response, enums.RollkeyMode)

	def set_roll_keymode(self, rollkeymode: enums.RollkeyMode) -> None:
		"""SCPI: SYSTem:BASE:DISPlay:ROLLkeymode \n
		Snippet: driver.system.display.set_roll_keymode(rollkeymode = enums.RollkeyMode.CURSors) \n
		No command help available \n
			:param rollkeymode: No help available
		"""
		param = Conversions.enum_scalar_to_str(rollkeymode, enums.RollkeyMode)
		self._core.io.write(f'SYSTem:BASE:DISPlay:ROLLkeymode {param}')

	# noinspection PyTypeChecker
	def get_language(self) -> enums.DisplayLanguage:
		"""SCPI: SYSTem:BASE:DISPlay:LANGuage \n
		Snippet: value: enums.DisplayLanguage = driver.system.display.get_language() \n
		No command help available \n
			:return: language: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:DISPlay:LANGuage?')
		return Conversions.str_to_scalar_enum(response, enums.DisplayLanguage)

	def set_language(self, language: enums.DisplayLanguage) -> None:
		"""SCPI: SYSTem:BASE:DISPlay:LANGuage \n
		Snippet: driver.system.display.set_language(language = enums.DisplayLanguage.AR) \n
		No command help available \n
			:param language: No help available
		"""
		param = Conversions.enum_scalar_to_str(language, enums.DisplayLanguage)
		self._core.io.write(f'SYSTem:BASE:DISPlay:LANGuage {param}')

	def clone(self) -> 'Display':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Display(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
