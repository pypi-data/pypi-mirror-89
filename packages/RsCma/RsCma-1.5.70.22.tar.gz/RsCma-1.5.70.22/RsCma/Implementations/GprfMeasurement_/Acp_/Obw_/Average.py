from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:ACP:OBW:AVERage \n
		Snippet: value: List[float] = driver.gprfMeasurement.acp.obw.average.fetch() \n
		Queries the OBW result. There are separate commands for the current, average and maximum value. CALCulate commands return
		error indicators instead of measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: obw: Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GPRF:MEASurement<Instance>:ACP:OBW:AVERage?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:GPRF:MEASurement<Instance>:ACP:OBW:AVERage \n
		Snippet: value: List[float] = driver.gprfMeasurement.acp.obw.average.read() \n
		Queries the OBW result. There are separate commands for the current, average and maximum value. CALCulate commands return
		error indicators instead of measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: obw: Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:GPRF:MEASurement<Instance>:ACP:OBW:AVERage?', suppressed)
		return response

	def calculate(self) -> List[float]:
		"""SCPI: CALCulate:GPRF:MEASurement<Instance>:ACP:OBW:AVERage \n
		Snippet: value: List[float] = driver.gprfMeasurement.acp.obw.average.calculate() \n
		Queries the OBW result. There are separate commands for the current, average and maximum value. CALCulate commands return
		error indicators instead of measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: obw: Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'CALCulate:GPRF:MEASurement<Instance>:ACP:OBW:AVERage?', suppressed)
		return response
