from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Item:
	"""Item commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("item", core, parent)

	def set(self, item_name: str, file_name: str) -> None:
		"""SCPI: MMEMory:STORe:ITEM \n
		Snippet: driver.massMemory.store.item.set(item_name = '1', file_name = '1') \n
		No command help available \n
			:param item_name: No help available
			:param file_name: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('item_name', item_name, DataType.String), ArgSingle('file_name', file_name, DataType.String))
		self._core.io.write(f'MMEMory:STORe:ITEM {param}'.rstrip())
