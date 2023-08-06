from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Maximum:
	"""Maximum commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("maximum", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:ACP:ACLR:MAXimum \n
		Snippet: value: List[float] = driver.gprfMeasurement.acp.aclr.maximum.fetch() \n
		Queries the ACLR results. There are separate commands for the current, average, maximum and standard deviation values.
		CALCulate commands return error indicators instead of measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: aclr: Comma-separated list of five ACLR values, one per channel: Channel -2, -1, 0, +1, +2 Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GPRF:MEASurement<Instance>:ACP:ACLR:MAXimum?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:GPRF:MEASurement<Instance>:ACP:ACLR:MAXimum \n
		Snippet: value: List[float] = driver.gprfMeasurement.acp.aclr.maximum.read() \n
		Queries the ACLR results. There are separate commands for the current, average, maximum and standard deviation values.
		CALCulate commands return error indicators instead of measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: aclr: Comma-separated list of five ACLR values, one per channel: Channel -2, -1, 0, +1, +2 Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:GPRF:MEASurement<Instance>:ACP:ACLR:MAXimum?', suppressed)
		return response

	def calculate(self) -> List[float]:
		"""SCPI: CALCulate:GPRF:MEASurement<Instance>:ACP:ACLR:MAXimum \n
		Snippet: value: List[float] = driver.gprfMeasurement.acp.aclr.maximum.calculate() \n
		Queries the ACLR results. There are separate commands for the current, average, maximum and standard deviation values.
		CALCulate commands return error indicators instead of measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: aclr: Comma-separated list of five ACLR values, one per channel: Channel -2, -1, 0, +1, +2 Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'CALCulate:GPRF:MEASurement<Instance>:ACP:ACLR:MAXimum?', suppressed)
		return response
