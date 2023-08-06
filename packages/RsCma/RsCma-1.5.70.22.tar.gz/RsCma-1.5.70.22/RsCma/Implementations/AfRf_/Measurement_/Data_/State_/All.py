from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class All:
	"""All commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("all", core, parent)

	# noinspection PyTypeChecker
	def fetch(self) -> List[enums.ResourceState]:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:DATA:STATe:ALL \n
		Snippet: value: List[enums.ResourceState] = driver.afRf.measurement.data.state.all.fetch() \n
		Queries the main measurement state and all substates. The substates provide additional information for the main state RUN. \n
			:return: meas_state: OFF | RUN | RDY | PENDing | ADJusted | QUEued | ACTive | INValid"""
		response = self._core.io.query_str(f'FETCh:AFRF:MEASurement<Instance>:DATA:STATe:ALL?')
		return Conversions.str_to_list_enum(response, enums.ResourceState)
