from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Frequency: List[float]: Frequency of the peak Unit: Hz
			- Level: List[float]: Level of the peak Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Frequency', DataType.FloatList, None, False, True, 1),
			ArgStruct('Level', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Frequency: List[float] = None
			self.Level: List[float] = None

	def read(self) -> ResultData:
		"""SCPI: READ:GPRF:MEASurement<Instance>:FFTSanalyzer:PEAKs:AVERage \n
		Snippet: value: ResultData = driver.gprfMeasurement.fftSpecAn.peaks.average.read() \n
		Queries the contents of the peak search result table. There are separate commands for the current and average spectrum
		traces. The results are returned in the following order: <Reliability>, {<Frequency>, <Level>}Peak 1, ..., {<Frequency>,
		<Level>}Peak 5 \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:GPRF:MEASurement<Instance>:FFTSanalyzer:PEAKs:AVERage?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:FFTSanalyzer:PEAKs:AVERage \n
		Snippet: value: ResultData = driver.gprfMeasurement.fftSpecAn.peaks.average.fetch() \n
		Queries the contents of the peak search result table. There are separate commands for the current and average spectrum
		traces. The results are returned in the following order: <Reliability>, {<Frequency>, <Level>}Peak 1, ..., {<Frequency>,
		<Level>}Peak 5 \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:GPRF:MEASurement<Instance>:FFTSanalyzer:PEAKs:AVERage?', self.__class__.ResultData())
