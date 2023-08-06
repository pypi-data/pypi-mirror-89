from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, sav_rcl_state_number: int, file_name: str, msus: str = None) -> None:
		"""SCPI: MMEMory:STORe:STATe \n
		Snippet: driver.massMemory.store.state.set(sav_rcl_state_number = 1, file_name = '1', msus = '1') \n
		Stores the instrument settings from the specified internal memory to the specified file. To store the current instrument
		settings to the memory, use *SAV <MemoryNumber> first. \n
			:param sav_rcl_state_number: No help available
			:param file_name: No help available
			:param msus: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sav_rcl_state_number', sav_rcl_state_number, DataType.Integer), ArgSingle('file_name', file_name, DataType.String), ArgSingle('msus', msus, DataType.String, True))
		self._core.io.write(f'MMEMory:STORe:STATe {param}'.rstrip())
