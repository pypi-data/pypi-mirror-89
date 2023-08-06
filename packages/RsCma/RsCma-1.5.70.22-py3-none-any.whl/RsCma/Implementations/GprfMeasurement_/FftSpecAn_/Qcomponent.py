from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Qcomponent:
	"""Qcomponent commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("qcomponent", core, parent)

	def read(self) -> List[float]:
		"""SCPI: READ:GPRF:MEASurement<Instance>:FFTSanalyzer:Q \n
		Snippet: value: List[float] = driver.gprfMeasurement.fftSpecAn.qcomponent.read() \n
		Queries the contents of the time domain diagrams. There are separate commands for the I amplitudes and the Q amplitudes. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: qdata: Comma-separated list of normalized I or Q amplitudes The number of values equals the configured FFT length. The order of the values corresponds to the I/Q vs. time diagram, from left to right."""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:GPRF:MEASurement<Instance>:FFTSanalyzer:Q?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:FFTSanalyzer:Q \n
		Snippet: value: List[float] = driver.gprfMeasurement.fftSpecAn.qcomponent.fetch() \n
		Queries the contents of the time domain diagrams. There are separate commands for the I amplitudes and the Q amplitudes. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: qdata: Comma-separated list of normalized I or Q amplitudes The number of values equals the configured FFT length. The order of the values corresponds to the I/Q vs. time diagram, from left to right."""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GPRF:MEASurement<Instance>:FFTSanalyzer:Q?', suppressed)
		return response
