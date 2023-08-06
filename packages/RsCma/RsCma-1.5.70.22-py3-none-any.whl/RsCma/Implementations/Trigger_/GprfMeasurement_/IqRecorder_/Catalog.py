from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Catalog:
	"""Catalog commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("catalog", core, parent)

	def get_source(self) -> List[str]:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:IQRecorder:CATalog:SOURce \n
		Snippet: value: List[str] = driver.trigger.gprfMeasurement.iqRecorder.catalog.get_source() \n
		Returns a list of all trigger source values that can be selected via method RsCma.Trigger.GprfMeasurement.IqRecorder.
		source. \n
			:return: trigger_sources: Comma-separated list of all strings, one string per source
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:IQRecorder:CATalog:SOURce?')
		return Conversions.str_to_str_list(response)
