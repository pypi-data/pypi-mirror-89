from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SaveState:
	"""SaveState commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("saveState", core, parent)

	def set(self, num: float) -> None:
		"""SCPI: *SAV \n
		Snippet: driver.saveState.set(num = 1.0) \n
		Stores the current instrument settings under the specified number in an intermediate memory. The settings can be restored,
		using the command *RCL with the associated number. To save the stored instrument settings to a file, see method RsCma.
		MassMemory.Store.State.set. See also MMEMory:SAV. \n
			:param num: Range: 0 to 99
		"""
		param = Conversions.decimal_value_to_str(num)
		self._core.io.write(f'*SAV {param}')
