from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Display:
	"""Display commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("display", core, parent)

	def get_update(self) -> bool:
		"""SCPI: SYSTem:DISPlay:UPDate \n
		Snippet: value: bool = driver.system.display.get_update() \n
		Defines whether the display is updated or not while the instrument is in the remote state. Disabling the update speeds up
		testing and is the recommended state. See also 'Using the Display during Remote Control'. \n
			:return: displayupdate: No help available
		"""
		response = self._core.io.query_str('SYSTem:DISPlay:UPDate?')
		return Conversions.str_to_bool(response)

	def set_update(self, displayupdate: bool) -> None:
		"""SCPI: SYSTem:DISPlay:UPDate \n
		Snippet: driver.system.display.set_update(displayupdate = False) \n
		Defines whether the display is updated or not while the instrument is in the remote state. Disabling the update speeds up
		testing and is the recommended state. See also 'Using the Display during Remote Control'. \n
			:param displayupdate: 1 | 0 1: The display is shown and updated during remote control. 0: The display shows static image during remote control.
		"""
		param = Conversions.bool_to_str(displayupdate)
		self._core.io.write(f'SYSTem:DISPlay:UPDate {param}')
