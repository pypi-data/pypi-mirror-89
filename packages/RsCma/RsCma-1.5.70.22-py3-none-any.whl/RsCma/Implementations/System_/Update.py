from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Update:
	"""Update commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("update", core, parent)

	def get_dgroup(self) -> str:
		"""SCPI: SYSTem:UPDate:DGRoup \n
		Snippet: value: str = driver.system.update.get_dgroup() \n
		No command help available \n
			:return: devicegroup: No help available
		"""
		response = self._core.io.query_str('SYSTem:UPDate:DGRoup?')
		return trim_str_response(response)

	def set_dgroup(self, devicegroup: str) -> None:
		"""SCPI: SYSTem:UPDate:DGRoup \n
		Snippet: driver.system.update.set_dgroup(devicegroup = '1') \n
		No command help available \n
			:param devicegroup: No help available
		"""
		param = Conversions.value_to_quoted_str(devicegroup)
		self._core.io.write(f'SYSTem:UPDate:DGRoup {param}')
