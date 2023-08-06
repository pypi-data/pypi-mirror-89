from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:FFTSanalyzer:POWer:CURRent \n
		Snippet: value: List[float] = driver.gprfMeasurement.fftSpecAn.power.current.fetch() \n
		Queries the contents of the spectrum diagram. There are separate commands for the current, average, minimum and maximum
		power traces. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power: Comma-separated list of 801 power values The power values cover the entire measured frequency span, from the lower end to the upper end. The frequency distance between two results equals span/800. Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GPRF:MEASurement<Instance>:FFTSanalyzer:POWer:CURRent?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:GPRF:MEASurement<Instance>:FFTSanalyzer:POWer:CURRent \n
		Snippet: value: List[float] = driver.gprfMeasurement.fftSpecAn.power.current.read() \n
		Queries the contents of the spectrum diagram. There are separate commands for the current, average, minimum and maximum
		power traces. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power: Comma-separated list of 801 power values The power values cover the entire measured frequency span, from the lower end to the upper end. The frequency distance between two results equals span/800. Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:GPRF:MEASurement<Instance>:FFTSanalyzer:POWer:CURRent?', suppressed)
		return response
