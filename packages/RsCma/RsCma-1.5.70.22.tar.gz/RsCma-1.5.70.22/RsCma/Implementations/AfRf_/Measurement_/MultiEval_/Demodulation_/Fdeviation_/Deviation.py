from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Deviation:
	"""Deviation commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("deviation", core, parent)

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Rms: float: RMS average value Unit: Hz
			- Rms_Sqrt_2: float: RMS result multiplied with the square root of 2 Unit: Hz
			- Ppeak: float: Positive peak value Unit: Hz
			- Mpeak: float: Negative peak value Unit: Hz
			- Mp_Peak_Average: enums.ResultStatus: Peak-to-peak value divided by 2 Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Rms'),
			ArgStruct.scalar_float('Rms_Sqrt_2'),
			ArgStruct.scalar_float('Ppeak'),
			ArgStruct.scalar_float('Mpeak'),
			ArgStruct.scalar_enum('Mp_Peak_Average', enums.ResultStatus)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Rms: float = None
			self.Rms_Sqrt_2: float = None
			self.Ppeak: float = None
			self.Mpeak: float = None
			self.Mp_Peak_Average: enums.ResultStatus = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:AFRF:MEASurement<Instance>:MEValuation:DEModulation:FDEViation:DEViation \n
		Snippet: value: CalculateStruct = driver.afRf.measurement.multiEval.demodulation.fdeviation.deviation.calculate() \n
		Queries the demodulation results for FM or FM stereo demodulation. A statistical evaluation of the frequency deviation or
		multiplex deviation is returned. CALCulate commands return error indicators instead of measurement values. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:AFRF:MEASurement<Instance>:MEValuation:DEModulation:FDEViation:DEViation?', self.__class__.CalculateStruct())

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Rms: float: RMS average value Unit: Hz
			- Rms_Sqrt_2: float: RMS result multiplied with the square root of 2 Unit: Hz
			- Ppeak: float: Positive peak value Unit: Hz
			- Mpeak: float: Negative peak value Unit: Hz
			- Mp_Peak_Average: float: Peak-to-peak value divided by 2 Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Rms'),
			ArgStruct.scalar_float('Rms_Sqrt_2'),
			ArgStruct.scalar_float('Ppeak'),
			ArgStruct.scalar_float('Mpeak'),
			ArgStruct.scalar_float('Mp_Peak_Average')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Rms: float = None
			self.Rms_Sqrt_2: float = None
			self.Ppeak: float = None
			self.Mpeak: float = None
			self.Mp_Peak_Average: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:DEModulation:FDEViation:DEViation \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.demodulation.fdeviation.deviation.fetch() \n
		Queries the demodulation results for FM or FM stereo demodulation. A statistical evaluation of the frequency deviation or
		multiplex deviation is returned. CALCulate commands return error indicators instead of measurement values. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:DEModulation:FDEViation:DEViation?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:DEModulation:FDEViation:DEViation \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.demodulation.fdeviation.deviation.read() \n
		Queries the demodulation results for FM or FM stereo demodulation. A statistical evaluation of the frequency deviation or
		multiplex deviation is returned. CALCulate commands return error indicators instead of measurement values. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:AFRF:MEASurement<Instance>:MEValuation:DEModulation:FDEViation:DEViation?', self.__class__.ResultData())
