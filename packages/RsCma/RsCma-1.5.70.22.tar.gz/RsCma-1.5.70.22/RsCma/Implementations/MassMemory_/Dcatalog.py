from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dcatalog:
	"""Dcatalog commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dcatalog", core, parent)

	@property
	def length(self):
		"""length commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_length'):
			from .Dcatalog_.Length import Length
			self._length = Length(self._core, self._base)
		return self._length

	def get(self, path_name: str = None) -> List[str]:
		"""SCPI: MMEMory:DCATalog \n
		Snippet: value: List[str] = driver.massMemory.dcatalog.get(path_name = '1') \n
		Returns the subdirectories of the specified directory. \n
			:param path_name: No help available
			:return: file_entry: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('path_name', path_name, DataType.String, True))
		response = self._core.io.query_str(f'MMEMory:DCATalog? {param}'.rstrip())
		return Conversions.str_to_str_list(response)

	def clone(self) -> 'Dcatalog':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dcatalog(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
