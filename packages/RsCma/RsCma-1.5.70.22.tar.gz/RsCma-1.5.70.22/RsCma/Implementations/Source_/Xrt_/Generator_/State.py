from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, gen_control: bool) -> None:
		"""SCPI: SOURce:XRT:GENerator<Instance>:STATe \n
		Snippet: driver.source.xrt.generator.state.set(gen_control = False) \n
		No command help available \n
			:param gen_control: No help available
		"""
		param = Conversions.bool_to_str(gen_control)
		self._core.io.write_with_opc(f'SOURce:XRT:GENerator<Instance>:STATe {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.GeneratorState:
		"""SCPI: SOURce:XRT:GENerator<Instance>:STATe \n
		Snippet: value: enums.GeneratorState = driver.source.xrt.generator.state.get() \n
		No command help available \n
			:return: gen_state: No help available"""
		response = self._core.io.query_str_with_opc(f'SOURce:XRT:GENerator<Instance>:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.GeneratorState)

	# noinspection PyTypeChecker
	def get_all(self) -> List[enums.GeneratorState]:
		"""SCPI: SOURce:XRT:GENerator<Instance>:STATe:ALL \n
		Snippet: value: List[enums.GeneratorState] = driver.source.xrt.generator.state.get_all() \n
		No command help available \n
			:return: all_states: No help available
		"""
		response = self._core.io.query_str('SOURce:XRT:GENerator<Instance>:STATe:ALL?')
		return Conversions.str_to_list_enum(response, enums.GeneratorState)
