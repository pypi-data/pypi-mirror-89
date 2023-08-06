from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Types import DataType
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Catalog:
	"""Catalog commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("catalog", core, parent)

	@property
	def length(self):
		"""length commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_length'):
			from .Catalog_.Length import Length
			self._length = Length(self._core, self._base)
		return self._length

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Used_Memory: int: No parameter help available
			- Free_Memory: int: No parameter help available
			- File_Entry: List[str]: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Used_Memory'),
			ArgStruct.scalar_int('Free_Memory'),
			ArgStruct('File_Entry', DataType.StringList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Used_Memory: int = None
			self.Free_Memory: int = None
			self.File_Entry: List[str] = None

	def get(self, path_name: str, format_py: enums.CatalogFormat = None) -> GetStruct:
		"""SCPI: MMEMory:CATalog \n
		Snippet: value: GetStruct = driver.massMemory.catalog.get(path_name = '1', format_py = enums.CatalogFormat.ALL) \n
		Returns information about the specified directory. \n
			:param path_name: No help available
			:param format_py: ALL | WTIme ALL Output enhanced with date, time and file attributes WTIme Output enhanced with date and time
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('path_name', path_name, DataType.String), ArgSingle('format_py', format_py, DataType.Enum, True))
		return self._core.io.query_struct(f'MMEMory:CATalog? {param}'.rstrip(), self.__class__.GetStruct())

	def clone(self) -> 'Catalog':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Catalog(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
