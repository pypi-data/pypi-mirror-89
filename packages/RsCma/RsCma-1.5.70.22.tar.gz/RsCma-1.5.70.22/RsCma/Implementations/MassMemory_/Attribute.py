from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Attribute:
	"""Attribute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("attribute", core, parent)

	def set(self, path_name: str, attributes: str) -> None:
		"""SCPI: MMEMory:ATTRibute \n
		Snippet: driver.massMemory.attribute.set(path_name = '1', attributes = '1') \n
		Sets or removes attributes for files and directories, or queries the attributes. \n
			:param path_name: No help available
			:param attributes: Attribute actions, separated by a blank + before an attribute: Sets the attribute. - before an attribute: Deletes the attribute. Possible attributes: R: read-only file A: archive file S: system file H: hidden file
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('path_name', path_name, DataType.String), ArgSingle('attributes', attributes, DataType.String))
		self._core.io.write(f'MMEMory:ATTRibute {param}'.rstrip())

	def get(self, path_name: str) -> List[str]:
		"""SCPI: MMEMory:ATTRibute \n
		Snippet: value: List[str] = driver.massMemory.attribute.get(path_name = '1') \n
		Sets or removes attributes for files and directories, or queries the attributes. \n
			:param path_name: No help available
			:return: file_entry: No help available"""
		param = Conversions.value_to_quoted_str(path_name)
		response = self._core.io.query_str(f'MMEMory:ATTRibute? {param}')
		return Conversions.str_to_str_list(response)
